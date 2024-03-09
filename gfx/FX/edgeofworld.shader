Includes = {
	"cw/pdxmesh.fxh"
	"cw/terrain.fxh"
	"cw/utility.fxh"
	"cw/pdxgui.fxh"
	"jomini/jomini_fog.fxh"
	"jomini/jomini_lighting.fxh"
	"jomini/jomini_mapobject.fxh"
	"cwp_coloroverlay.fxh"
	"distance_fog.fxh"
	"fog_of_war.fxh"
	"sharedconstants.fxh"
	"edgeofworld.fxh"
}

VertexStruct VS_OUTPUT_EDGEOFWORLD
{
	float4 Position			: PDX_POSITION;
	float3 WorldSpacePos	: TEXCOORD0;
	float2 UV01				: TEXCOORD1;
};

VertexShader =
{
	Code
	[[
		float3 QRotVector( float4 RotQ, float3 V )
		{
			return V + 2.0 * cross( RotQ.xyz, cross( RotQ.xyz, V ) + RotQ.w * V );
		}

		VS_OUTPUT_EDGEOFWORLD ConvertOutput( VS_OUTPUT_PDXMESH MeshOutput )
		{
			VS_OUTPUT_EDGEOFWORLD Output;

			Output.WorldSpacePos = MeshOutput.WorldSpacePos;
			Output.WorldSpacePos.y += 1.0f;
			Output.Position = FixProjectionAndMul( ViewProjectionMatrix, float4( Output.WorldSpacePos, 1.0 ) );
			Output.UV01 = float2( MeshOutput.WorldSpacePos.x / MapSize.x, 1.0 - MeshOutput.WorldSpacePos.z / MapSize.y );

			return Output;
		}
	]]
	MainCode VS_edgeofworld_mesh
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT_EDGEOFWORLD"
		Code
		[[
			PDX_MAIN
			{
				return ConvertOutput( PdxMeshVertexShaderStandard( Input ) );
			}
		]]
	}
	MainCode VS_edgeofworld_mapobject
	{
		Input = "VS_INPUT_PDXMESH_MAPOBJECT"
		Output = "VS_OUTPUT_EDGEOFWORLD"
		Code
		[[
			PDX_MAIN
			{
				return ConvertOutput( PdxMeshVertexShader( PdxMeshConvertInput( Input ), 0, UnpackAndGetMapObjectWorldMatrix( Input.InstanceIndex24_Opacity8 ) ) );
			}
		]]
	}
}

PixelShader =
{
	MainCode GameEdgeOfWorldShader
	{
		Input = "VS_OUTPUT_EDGEOFWORLD"
		Output = "PDX_COLOR"
		Code
		[[

			PDX_MAIN
			{

				float2 UV = Input.UV01;

				float Alpha = 1.0f - _FlatmapLerp;
				PdxMeshApplyDitheredOpacity( Alpha, UV );
				clip( Alpha - 0.001f );

				// Base cloud layer
				float2 BaseCloudUV = float2( UV.x * _EowConstants._BaseCloudTileFactor, UV.y * ( _EowConstants._BaseCloudTileFactor / 2.0f ) );
				float2 BaseCloudOffset = GlobalTime * _EowConstants._BaseCloudScrolling;
				float2 AnimatedBaseCloudUV = BaseCloudUV + BaseCloudOffset;

				// Cloud layers
				float CloudAlpha = PdxTex2D( EdgeOfWorldTexture, AnimatedBaseCloudUV ).r;
				float CloudAlpha2 = PdxTex2D( EdgeOfWorldTexture, ( AnimatedBaseCloudUV + GlobalTime * _EowConstants._Cloud1Scrolling ) * _EowConstants._Cloud1TileFactor ).r;
				float CloudAlpha3 = PdxTex2D( EdgeOfWorldTexture, ( AnimatedBaseCloudUV + GlobalTime * _EowConstants._Cloud2Scrolling ) * _EowConstants._Cloud2TileFactor ).r;
				CloudAlpha = LevelsScan( CloudAlpha, _EowConstants._BaseCloudPosition, _EowConstants._BaseCloudContrast );
				CloudAlpha2 = LevelsScan( CloudAlpha2, _EowConstants._Cloud1Position, _EowConstants._Cloud1Contrast );
				CloudAlpha3 = LevelsScan( CloudAlpha3, _EowConstants._Cloud2Position, _EowConstants._Cloud2Contrast );

				// Color
				float3 CloudColor = lerp( _EowConstants._LowCloudColor.rgb, _EowConstants._HighCloudColor.rgb, CloudAlpha * _EowConstants._BaseCloudStrength + CloudAlpha2 * _EowConstants._Cloud1Strength + CloudAlpha3 * _EowConstants._Cloud2Strength );

				float3 Normal = normalize( float3( 0.0f, 1.0f, 0.0f ) );
				SMaterialProperties MaterialProps = GetMaterialProperties( CloudColor, Normal, 0.8, 0.16, 1.0 );
				SLightingProperties LightingProps = GetSunLightingProperties( Input.WorldSpacePos, 1.0 );

				float3 Color = CalculateSunLighting( MaterialProps, LightingProps, EnvironmentMap );
				Color = ApplyDistanceFog( Color, Input.WorldSpacePos );
				Color *= _EowConstants._ColorMultiply;

				// Edge fade
				float FadeDist = _EowConstants._FadeDistance;
				float FadeTop = Input.WorldSpacePos.z - MapSize.y + 10.0f + FadeDist;
				FadeTop = smoothstep(0.0f, FadeDist, FadeTop);
				float FadeBottom = FadeDist - Input.WorldSpacePos.z;
				FadeBottom = smoothstep( 0.0f, FadeDist, FadeBottom);
				Alpha *= FadeTop + FadeBottom;

				return float4( Color, Alpha );
			}
		]]
	}

	MainCode GameEdgeOfWorldPapermapShader
	{
		Input = "VS_OUTPUT_EDGEOFWORLD"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float2 UV = Input.UV01;

				float3 defaultcolor = float3( 0.020, 0.015, 0.01 );
				float ColorMult = 1.0f;
				float SizeMult = 0.2f;
				float LightWeight = 0.0f;

				// Paralx Coord
				float3 ToCam = normalize( CameraPosition - Input.WorldSpacePos );
				float ParalaxDist = ( -2000.0f - Input.WorldSpacePos.y ) / ToCam.y;
				float ParalaxDist2 = ( -1000.0f - Input.WorldSpacePos.y ) / ToCam.y;
				float ParalaxDist3 = ( -300.0f - Input.WorldSpacePos.y ) / ToCam.y;
				float ParalaxDist4 = ( 300.0f - Input.WorldSpacePos.y ) / ToCam.y;

				float2 uv = float2( ( Input.UV01.x * 2.0f ) - 0.5f, Input.UV01.y );

				float2 p = ( ( uv - 0.5f ) * 200000 * SizeMult );
				float2 p2 = ( ( uv - 0.5f ) * 60000 * SizeMult );
				float2 p3 = ( ( uv - 0.5f ) * 45000 * SizeMult );
				float2 p4 = ( ( uv - 0.5f ) * 30000 * SizeMult );
				p = p + ToCam * ParalaxDist;
				p2 = p2 + ToCam * ParalaxDist2;
				p3 = p3 + ToCam * ParalaxDist3;
				p4 = p4 + ToCam * ParalaxDist4;

				// Circle layers
				float3 color = defaultcolor;
				Rotate2( p, 0.2 );
				BokehLayerSmall( color, p + float2( 100000.0, 100000.0 ), 0.02 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );
				Rotate2( p, 0.3 );
				BokehLayerSmall( color, p + float2( 100000.0, 100000.0 ), 0.02 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );
				Rotate2( p, 0.5 );
				BokehLayerSmall( color, p + float2( 100000.0, 100000.0 ), 0.001 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );

				Rotate2( p2, 1.0 );
				BokehLayerMedium( color, p2 + float2( 100000.0, 100000.0 ), 0.004 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );
				Rotate2( p2, 2.0 );
				BokehLayerMedium( color, p2 + float2( 100000.0, 100000.0 ), 0.004 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );

				Rotate2( p3, 3.0 );
				BokehLayerMedium2( color, p3 + float2( 100000.0, 100000.0 ), 0.004 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );
				Rotate2( p3, 8.0 );
				BokehLayerMedium2( color, p3 + float2( 100000.0, 100000.0 ), 0.004 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );

				Rotate2( p4, 0.1 );
				BokehLayerLarge( color, p4 + float2( 100000.0, 100000.0 ), 0.008 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );
				Rotate2( p4, 0.5 );
				BokehLayerLarge( color, p4 + float2( 100000.0, 100000.0 ), 0.008 * ColorMult * float3( 0.5, 0.3, 0.1 ), LightWeight );


				float3 Normal = normalize( float3( 0.0f, 1.0f, 0.0f ) );
				SMaterialProperties MaterialProps = GetMaterialProperties( color, Normal, 0.3f, 0.16f, 0.0f );
				SLightingProperties LightingProps = GetSunLightingProperties( Input.WorldSpacePos, 1.0f );
				LightingProps._LightIntensity = float3( 0.5, 0.3, 0.1 ) * 28.0f;
				LightingProps._ToLightDir = float3( -0.2, 0.5, 0.8 );

				float3 Color = CalculateSunLighting( MaterialProps, LightingProps, EnvironmentMap );

				// Edge fade
				float Alpha = 1.0f;
				float FadeDistance = 5000.0f;

				float FadeRight = MapSize.x - Input.WorldSpacePos.x - FadeDistance;
				FadeRight = smoothstep( -FadeDistance, 0.0f, FadeRight );
				float FadeLeft = FadeDistance - Input.WorldSpacePos.x;
				FadeLeft = smoothstep( FadeDistance, 0.0f, FadeLeft );
				LightWeight *= FadeRight * FadeLeft;

				Color = lerp( defaultcolor, Color, saturate( LightWeight ) );

				return float4( Color, 1.0 );
			}
		]]
	}
}


#// Render settings
BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
	WriteMask = "RED|GREEN|BLUE"
}

DepthStencilState StandardDepthStencilState
{
	DepthEnable = yes
	DepthWriteEnable = yes
}

DepthStencilState NoDepthCheck
{
	#// Always render on top
	DepthEnable = no
	DepthWriteEnable = no
}


#// Shaders
Effect edgeofworld
{
	VertexShader = "VS_edgeofworld_mesh"
	PixelShader = "GameEdgeOfWorldShader"

	DepthStencilState = NoDepthCheck
}

Effect edgeofworld_papermap
{
	VertexShader = "VS_edgeofworld_mesh"
	PixelShader = "GameEdgeOfWorldPapermapShader"

	DepthStencilState = StandardDepthStencilState
}


#// Mapobject Shaders
Effect edgeofworld_mapobject
{
	VertexShader = "VS_edgeofworld_mapobject"
	PixelShader = "GameEdgeOfWorldShader"

	DepthStencilState = NoDepthCheck
}

Effect edgeofworld_papermap_mapobject
{
	VertexShader = "VS_edgeofworld_mapobject"
	PixelShader = "GameEdgeOfWorldPapermapShader"

	DepthStencilState = StandardDepthStencilState
}
