Includes = {
	"cw/pdxterrain.fxh"
	"cw/camera.fxh"
	"cw/shadow.fxh"
	"jomini/jomini_flat_border.fxh"
	"jomini/jomini_lighting.fxh"
	"sharedconstants.fxh"
	"distance_fog.fxh"
	"fog_of_war.fxh"
	"ssao_struct.fxh"
	"pdxverticalborder.fxh"
	"dynamic_masks.fxh"
}

VertexStruct VS_OUTPUT_PDX_BORDER
{
	float4 Position			: PDX_POSITION;
	float3 WorldSpacePos	: TEXCOORD0;
	float2 UV				: TEXCOORD1;
};


TextureSampler EnvironmentMap
{
	Ref = JominiEnvironmentMap
	MagFilter = "Linear"
	MinFilter = "Linear"
	MipFilter = "Linear"
	SampleModeU = "Clamp"
	SampleModeV = "Clamp"
	Type = "Cube"
}

VertexShader =
{
	MainCode VertexShader
	{
		Input = "VS_INPUT_PDX_BORDER"
		Output = "VS_OUTPUT_PDX_BORDER"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_PDX_BORDER Out;

				float3 position = Input.Position.xyz;
				position.y = lerp( position.y, FlatMapHeight, FlatMapLerp );
				position.y += _HeightOffset;

				Out.WorldSpacePos = position;
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, float4( position, 1.0 ) );
				Out.UV = Input.UV;

				return Out;
			}
		]]
	}
}

PixelShader =
{
	TextureSampler BorderTexture
	{
		Ref = PdxTexture0
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler CountryColors
	{
		Ref = CountryColors
		MagFilter = "Point"
		MinFilter = "Point"
		MipFilter = "Point"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler ShadowMap
	{
		Ref = PdxShadowmap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
		CompareFunction = less_equal
		SamplerType = "Compare"
	}
	
	MainCode BorderPs
	{
		Input = "VS_OUTPUT_PDX_BORDER"
		Output = "PS_COLOR_SSAO"
		Code
		[[
			PDX_MAIN
			{
				PS_COLOR_SSAO Out;

				float4 Diffuse = PdxTex2D( BorderTexture, Input.UV );

				#ifdef COUNTRY_COLOR
					float4 CountryColor = PdxTex2DLoad0( CountryColors, int2( _UserId, 0 ) );
					Diffuse.rgb *= CountryColor.rgb;
					Diffuse.rgb *= 1.0f - FlatMapLerp;
					Diffuse.a = lerp( Diffuse.a, 0.5f, FlatMapLerp );
				#endif

				#ifdef IMPASSABLE_BORDER
					Diffuse.rgb *= ImpassableTerrainColor.rgb;
				#endif

				if( FlatMapLerp < 1.0f )
				{
					float3 Unfogged = Diffuse.rgb;
					Diffuse.rgb = ApplyFogOfWar( Diffuse.rgb, Input.WorldSpacePos );
					Diffuse.rgb = GameApplyDistanceFog( Diffuse.rgb, Input.WorldSpacePos );
					Diffuse.rgb = lerp( Diffuse.rgb, Unfogged, FlatMapLerp );
				}

				// Close fadeout
				float FadeStart = ( DistanceFadeStart - DistanceFadeEnd );
				float CloseZoomBlend = FadeStart - CameraPosition.y + ( DistanceFadeEnd );
				CloseZoomBlend = smoothstep( FadeStart, 0.0f, CloseZoomBlend );
				Diffuse.a *= CloseZoomBlend;

				Diffuse.a *= _Alpha;

				// Output
				Out.Color = Diffuse;

				// Process to mask out SSAO where borders become opaque, using SSAO color
				Out.SSAOColor = float4( 1.0f, 1.0f, 1.0f, Diffuse.a );

				return Out;
			}
		]]
	}

	TextureSampler BorderTexture0
	{
		Ref = JominiVerticalBordersMask0
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}

	MainCode FlatWarBorderPs
	{
		Input = "VS_OUTPUT_PDX_BORDER"
		Output = "PS_COLOR_SSAO"
		Code
		[[

			// Flatmap
			#define ANIMATION_SPEED float2( 3.0, 1.0f )
			#define UV_TILING 8

			#define NOISE_MASK_POSITION 1.3f
			#define NOISE_MASK_CONTRAST 2.3f

			#define COLOR_1 float3( 1.0f, 0.02f, 0.0f )
			#define COLOR_2 float3( 1.0f, 1.0f, 0.0f )
			#define COLOR_INTENSITY 2.5f

			#define EDGE_FADE_DISTANCE 0.8
			#define EDGE_FADE_SHARPNESS 5.0
		
			// Ground flames
			#define FLAME_FADE_DISTANCE 0.64
			#define FLAME_FADE_SHARPNESS 10.0

			// Center Flame
			#define FLAME_CENTER_INTENSITY 1.0
			#define FLAME_CENTER_DISTANCE 0.54
			#define FLAME_CENTER_SHARPNESS 20.0
			#define FLAME_CENTER_HEIGHTFACTOR_POSITION 0.4
			#define FLAME_CENTER_HEIGHTFACTOR_CONTRAST 0.4

			// Base Mask
			#define FLAME_MASK_INTENSITY 1.5
			#define FLAME_DEVASTATION_INTENSITY FLAME_MASK_INTENSITY * 1.0

			#define FLAME_HEIGHTFACTOR_POSITION 0.9
			#define FLAME_HEIGHTFACTOR_CONTRAST 1.5

			// Color - Emissive
			#define FLAME_SATURATION 1.04
			#define FLAME_EMISSIVE 1.5

			void ApplyFlatmapDiffuse( inout float3 Diffuse, inout float Alpha, float2 WorldSpacePosXZ, float2 UV )
			{
				float2 WorldUV = WorldSpacePosXZ;
				float2 AnimUVs = float2( WorldUV.x, -WorldUV.y ) - GlobalTime * ANIMATION_SPEED;
				AnimUVs = AnimUVs * UV_TILING * 0.001f;

				// Noise
				float NoiseLayer = PdxTex2D( BorderTexture, AnimUVs ).a;
				NoiseLayer = saturate( LevelsScan( NoiseLayer, NOISE_MASK_POSITION, NOISE_MASK_CONTRAST ) );
				
				// Color
				float4 BottomLayer = float4( COLOR_1, 1.0f );
				float4 Color1Layer = float4( COLOR_2, NoiseLayer );
				BottomLayer.rgb *= COLOR_INTENSITY;
				Color1Layer.rgb *= COLOR_INTENSITY;
				float3 FlatmapDiffuse =  AlphaBlendAOverB( Color1Layer, BottomLayer );
				
				// Alpha
				float FadeRight = UV.y;
				FadeRight = saturate( ( EDGE_FADE_DISTANCE - FadeRight) * EDGE_FADE_SHARPNESS );
				float FadeLeft = 1.0f - UV.y;
				FadeLeft = saturate( ( EDGE_FADE_DISTANCE - FadeLeft ) * EDGE_FADE_SHARPNESS );
				float FlatmapAlpha = FadeRight * FadeLeft;
				
				Diffuse = lerp( Diffuse, FlatmapDiffuse, FlatMapLerp );
				Alpha = lerp( Alpha, FlatmapAlpha, FlatMapLerp );
			}

			float GetFade( float2 UV, float Distance, float Sharpness )
			{
				float FadeRight = UV.y;
				FadeRight = saturate( ( Distance - FadeRight) * Sharpness );
				float FadeLeft = 1.0f - UV.y;
				FadeLeft = saturate( ( Distance - FadeLeft ) * Sharpness );
				float Fade = FadeLeft * FadeRight;

				return Fade;
			}

			float3 ApplyDevastationMaterialVFXBorder( inout float4 Diffuse, float2 UV, float FlameMask )
			{
				// Effect Properties
				float FireUVDistortionStrength = 0.5f;
				float2 PanSpeedA = float2( 0.005, 0.001 );
				float2 PanSpeedB = float2( 0.010, 0.005 );

				// UV & UV Panning Properties
				float2 UVPan02 = float2( -frac( GlobalTime * PanSpeedA.x ), frac( GlobalTime * PanSpeedA.y ) );
				float2 UVPan01 = float2( frac( GlobalTime * PanSpeedB.x ),  frac( GlobalTime * PanSpeedB.y ) );
				float2 UV02 = ( UV + 0.5 ) * 0.1;
				float2 UV01 = UV * 0.2;

				// Pan and Sample noise for UV distortion
				UV02 += UVPan02;
				float DevastationAlpha02 = PdxTex2D( DevastationPollution, float3( UV02, DevastationTexIndex + DevastationTexIndexOffset ) ).a;

				// Apply the UV Distortion
				UV01 += UVPan01;
				UV01 += DevastationAlpha02 * FireUVDistortionStrength;
				float DevastationAlpha01 = PdxTex2D( DevastationPollution, float3( UV01, DevastationTexIndex + DevastationTexIndexOffset ) ).a;

				// Adjust Mask Value ranges to clamp the effect
				DevastationAlpha01 = max( smoothstep( 0.2, 0.6, DevastationAlpha01 ), 0.5 );

				// Calculate the effect masks
				FlameMask = saturate( FlameMask * DevastationAlpha01 );

				float LutCoord = RemapClamped( FlameMask, 0.0, 1.0, -1.0, 0.84 );
				float3 FlameColor = PdxTex2D( VerticalBorderLUT , saturate( float2( LutCoord, 0.0 ) ) ).rgb;
				FlameColor *= FlameMask;

				float3 HSV_ = RGBtoHSV( FlameColor );
				HSV_.y *= FLAME_SATURATION;
				FlameColor = HSVtoRGB( HSV_ );

				FlameColor *= FLAME_EMISSIVE;

				return FlameColor;
			}

			PDX_MAIN
			{
				PS_COLOR_SSAO Out;

				float Alpha = 1.0f;

				// UVs
				float2 MapCoordinates = Input.WorldSpacePos.xz * WorldSpaceToTerrain0To1;
				float2 DetailUV = CalcDetailUV( Input.WorldSpacePos.xz );

				// Get terrain material
				float4 Diffuse;
				float3 Normal;
				float4 Properties;
				CalculateDetails( Input.WorldSpacePos.xz, Diffuse, Normal, Properties );
				
				float3 ColorMap = PdxTex2D( ColorTexture, float2( MapCoordinates.x, 1.0 - MapCoordinates.y ) ).rgb;
				Diffuse.rgb = SoftLight( Diffuse.rgb, ColorMap, ( 1.0 - Diffuse.r ) );

				float3 TerrainNormal = CalculateNormal( Input.WorldSpacePos.xz );
				Normal = ReorientNormal( TerrainNormal, Normal );

				// Get Devastation materials
				float4 DevDiffuse = PdxTex2D( DetailTextures, float3( DetailUV, DevastationTexIndex + DevastationTexIndexOffset ) );
				float4 DevProperties = PdxTex2D( MaterialTextures, float3( DetailUV, DevastationTexIndex + DevastationTexIndexOffset ) );
				float4 DevNormalRRxG = PdxTex2D( NormalTextures, float3( DetailUV, DevastationTexIndex + DevastationTexIndexOffset ) );
				float3 DevNormal = UnpackRRxGNormal( DevNormalRRxG ).xyz;
				DevNormal = ReorientNormal( Normal, DevNormal );

				// Devastation value
				float Devastation = saturate( GetDevastation( MapCoordinates ) * 5.0 );
				Devastation *= GetDevastationExclusionMask( MapCoordinates );

				// Devastation material
				Diffuse.rgb = lerp( Diffuse.rgb, DevDiffuse.rgb, Devastation );
				Properties = lerp( Properties, DevProperties, Devastation );
				Normal = lerp( Normal, DevNormal, Devastation );

				// Ground Flame mask
				Diffuse.a = lerp( 1.0 - Diffuse.a, Overlay( 1.0 - Diffuse.a, DevDiffuse.a ), Devastation );

				float CenterFlame = saturate( GetFade( Input.UV, FLAME_CENTER_DISTANCE, FLAME_CENTER_SHARPNESS ) * FLAME_CENTER_INTENSITY );
				float FlameContrast = lerp( FLAME_HEIGHTFACTOR_CONTRAST, FLAME_CENTER_HEIGHTFACTOR_CONTRAST, CenterFlame );
				float FlamePosition = lerp( FLAME_HEIGHTFACTOR_POSITION, FLAME_CENTER_HEIGHTFACTOR_POSITION, CenterFlame );

				// Mask Intensity
				float FlameMask = LevelsScan( Diffuse.a, FlamePosition, FlameContrast );
				float FlameFade = GetFade( Input.UV, FLAME_FADE_DISTANCE, FLAME_FADE_SHARPNESS );
				FlameMask *= lerp( FLAME_MASK_INTENSITY, FLAME_DEVASTATION_INTENSITY, Devastation ) * FlameFade;

				// Light calculation (terrain)
				SMaterialProperties MaterialProps = GetMaterialProperties( Diffuse.rgb, Normal, Properties.a, Properties.g, Properties.b );
				SLightingProperties LightingProps = GetSunLightingProperties( Input.WorldSpacePos, ShadowMap );
				Diffuse.rgb = CalculateSunLighting( MaterialProps, LightingProps, EnvironmentMap );

				// Apply Flame emissive
				Diffuse.rgb += ApplyDevastationMaterialVFXBorder( Diffuse, DetailUV, FlameMask );

				// Effects
				if( FlatMapLerp < 1.0f )
				{
					Diffuse.rgb = ApplyFogOfWar( Diffuse.rgb, Input.WorldSpacePos, 1.0 - FlameMask );
					Diffuse.rgb = GameApplyDistanceFog( Diffuse.rgb, Input.WorldSpacePos );
				}
				
				// Fade alpha
				float EdgeFade = lerp( FlameFade, GetFade( Input.UV, EDGE_FADE_DISTANCE, EDGE_FADE_SHARPNESS ), FlatMapLerp );
				Alpha *= EdgeFade;

				// Flatmap
				ApplyFlatmapDiffuse( Diffuse.rgb, Alpha, Input.WorldSpacePos.xz, Input.UV );

				// Output
				Out.Color.rgb = Diffuse.rgb;
				Out.Color.a = Alpha;

				// Process to mask out SSAO where borders become opaque, using SSAO color
				Out.SSAOColor = float4( 1.0f, 1.0f, 1.0f, Alpha );

				DebugReturn( Out.Color.rgb, MaterialProps, LightingProps, EnvironmentMap );
				return Out;
			}
		]]
	}
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
	WriteMask = "RED|GREEN|BLUE"
}

RasterizerState RasterizerState
{
	DepthBias = -300
	SlopeScaleDepthBias = -10
}

DepthStencilState DepthStencilState
{
	DepthEnable = yes
	DepthWriteEnable = no
}

Effect DefaultBorder
{
	VertexShader = "VertexShader"
	PixelShader = "BorderPs"
}
Effect CountryBorder
{
	VertexShader = "VertexShader"
	PixelShader = "BorderPs"
	Defines = { "COUNTRY_COLOR" }
}
Effect ImpassableBorder
{
	VertexShader = "VertexShader"
	PixelShader = "BorderPs"
	Defines = { "IMPASSABLE_BORDER" }
}
Effect FlatWarBorder
{
	VertexShader = "VertexShader"
	PixelShader = "FlatWarBorderPs"
}
