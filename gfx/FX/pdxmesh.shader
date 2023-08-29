Includes = {
	"cw/pdxmesh.fxh"
	"cw/terrain.fxh"
	"cw/utility.fxh"
	"cw/curve.fxh"
	"cw/shadow.fxh"
	"cw/camera.fxh"
	"cw/heightmap.fxh"
	"cw/alpha_to_coverage.fxh"
	"jomini/jomini_lighting.fxh"
	"jomini/jomini_water.fxh"
	"jomini/jomini_mapobject.fxh"
	"jomini/jomini_province_overlays.fxh"
	"dynamic_masks.fxh"
	"pdxmesh_functions.fxh"
	"sharedconstants.fxh"
	"fog_of_war.fxh"
	"distance_fog.fxh"
	"cwp_coloroverlay.fxh"
	"ssao_struct.fxh"
	"constants_ig_colors.fxh"
}

PixelShader =
{
	TextureSampler DiffuseMap
	{
		Ref = PdxTexture0
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}

	TextureSampler PropertiesMap
	{
		Ref = PdxTexture1
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}

	TextureSampler NormalMap
	{
		Ref = PdxTexture2
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}

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

	TextureSampler TintMap
	{
		Index = 5
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
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
}

VertexStruct VS_OUTPUT
{
	float4 Position			: PDX_POSITION;
	float3 Normal			: TEXCOORD0;
	float3 Tangent			: TEXCOORD1;
	float3 Bitangent		: TEXCOORD2;
	float2 UV0				: TEXCOORD3;
	float2 UV1				: TEXCOORD4;
	float3 WorldSpacePos	: TEXCOORD5;
	uint InstanceIndex 	: TEXCOORD6;
};

Code
[[
	uint GetUserDataUint( uint InstanceIndex )
	{
		return uint( Data[ InstanceIndex + PDXMESH_USER_DATA_OFFSET + 0 ].x );
	}
	float4 GetUserDataBuildingLightColor( uint InstanceIndex )
	{
		return Data[ InstanceIndex + PDXMESH_USER_DATA_OFFSET + 0 ];
	}
	float GetUserDataPrettyValue( uint InstanceIndex )
	{
		return Data[ InstanceIndex + PDXMESH_USER_DATA_OFFSET + 1 ].x;
	}
	float GetUserDataRandomValueCity( uint InstanceIndex )
	{
		return Data[ InstanceIndex + PDXMESH_USER_DATA_OFFSET + 1 ].y;
	}
	float GetUserDataShouldLightActivate( uint InstanceIndex )
	{
		return Data[ InstanceIndex + PDXMESH_USER_DATA_OFFSET + 1 ].z;
	}
]]

VertexShader =
{
	Code
	[[
		VS_OUTPUT ConvertOutput( VS_OUTPUT_PDXMESH In )
		{
			VS_OUTPUT Out;

			Out.Position = In.Position;
			Out.Normal = In.Normal;
			Out.Tangent = In.Tangent;
			Out.Bitangent = In.Bitangent;
			Out.UV0 = In.UV0;
			Out.UV1 = In.UV1;
			Out.WorldSpacePos = In.WorldSpacePos;
			return Out;
		}
	]]

	MainCode VS_standard
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT"
		Code
		[[
			PDX_MAIN
			{
				float4x4 WorldMatrix = PdxMeshGetWorldMatrix( Input.InstanceIndices.y );

				#ifdef WINDTRANSFORM
					#if defined( TREE_BUSH )
						Input.Position = WindTransformBush( Input.Position, WorldMatrix );
					#elif defined( TREE_MEDIUM )
						Input.Position = WindTransformMedium( Input.Position, WorldMatrix );
					#elif defined( TREE_TALL )
						Input.Position = WindTransformTall( Input.Position, WorldMatrix );
					#else
						Input.Position = WindTransform( Input.Position, WorldMatrix );
					#endif
				#endif

				#ifdef SNAP_TO_WATER
					Input.Position.y = SnapToWaterLevel( Input.Position.y, WorldMatrix );
				#endif

				VS_OUTPUT Out = ConvertOutput( PdxMeshVertexShaderStandard( Input ) );
				Out.InstanceIndex = Input.InstanceIndices.y;

				#ifdef PDX_MESH_SNAP_VERTICES_TO_TERRAIN
					Out.Normal = SimpleRotateNormalToTerrain( Out.Normal, Out.WorldSpacePos.xz );
				#endif

				return Out;
			}
		]]
	}
	MainCode VS_standard_shadow
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT_PDXMESHSHADOWSTANDARD"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_PDXMESHSHADOWSTANDARD Out;

				#ifdef SNAP_TO_WATER
					float4x4 WorldMatrix = PdxMeshGetWorldMatrix( Input.InstanceIndices.y );
					Input.Position.y = SnapToWaterLevel( Input.Position.y, WorldMatrix );
				#endif

				Out = PdxMeshVertexShaderShadowStandard( Input );
				return Out;
			}
		]]
	}

	MainCode VS_mapobject
	{
		Input = "VS_INPUT_PDXMESH_MAPOBJECT"
		Output = "VS_OUTPUT"
		Code
		[[
			PDX_MAIN
			{
				float4x4 WorldMatrix = UnpackAndGetMapObjectWorldMatrix( Input.InstanceIndex24_Opacity8 );

				#ifdef WINDTRANSFORM
					#if defined( TREE_BUSH )
						Input.Position = WindTransformBush( Input.Position, WorldMatrix );
					#elif defined( TREE_MEDIUM )
						Input.Position = WindTransformMedium( Input.Position, WorldMatrix );
					#elif defined( TREE_TALL )
						Input.Position = WindTransformTall( Input.Position, WorldMatrix );
					#else
						Input.Position = WindTransform( Input.Position, WorldMatrix );
					#endif
				#endif

				#ifdef SNAP_TO_WATER
					Input.Position.y = SnapToWaterLevel( Input.Position.y, WorldMatrix );
				#endif

				VS_OUTPUT Out = ConvertOutput( PdxMeshVertexShader( PdxMeshConvertInput( Input ), 0/*Not supported*/, UnpackAndGetMapObjectWorldMatrix( Input.InstanceIndex24_Opacity8 ) ) );
				Out.InstanceIndex = Input.InstanceIndex24_Opacity8;

				#ifdef PDX_MESH_SNAP_VERTICES_TO_TERRAIN
					Out.Normal = SimpleRotateNormalToTerrain( Out.Normal, Out.WorldSpacePos.xz );
				#endif

				return Out;
			}
		]]
	}
	MainCode VS_mapobject_shadow
	{
		Input = "VS_INPUT_PDXMESH_MAPOBJECT"
		Output = "VS_OUTPUT_MAPOBJECT_SHADOW"
		Code
		[[
			PDX_MAIN
			{
				uint InstanceIndex;
				float Opacity;
				UnpackMapObjectInstanceData( Input.InstanceIndex24_Opacity8, InstanceIndex, Opacity );
				float4x4 WorldMatrix = GetWorldMatrixMapObject( InstanceIndex );

				#ifdef SNAP_TO_WATER
					Input.Position.y = SnapToWaterLevel( Input.Position.y, WorldMatrix );
				#endif

				VS_OUTPUT_MAPOBJECT_SHADOW Out = ConvertOutputMapObjectShadow( PdxMeshVertexShaderShadow( PdxMeshConvertInput( Input ), 0/*Not supported*/, WorldMatrix ) );
				Out.InstanceIndex24_Opacity8 = Input.InstanceIndex24_Opacity8;
				return Out;
			}
		]]
	}

	MainCode VS_sine_animation
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT Out;

				float4 Position = float4( Input.Position.xyz, 1.0 );
				float4x4 WorldMatrix = PdxMeshGetWorldMatrix( Input.InstanceIndices.y );

				// Reset Rotation
				WorldMatrix[0][0] = 1;
				WorldMatrix[0][1] = 0;
				WorldMatrix[0][2] = 0;
				WorldMatrix[1][0] = 0;
				WorldMatrix[1][1] = 1;
				WorldMatrix[1][2] = 0;
				WorldMatrix[2][0] = 0;
				WorldMatrix[2][1] = 0;
				WorldMatrix[2][2] = 1;

				// Wave animation
				CalculateSineAnimation( Input.UV1, Position.xyz, Input.Normal, Input.Tangent, float3( GetMatrixData( WorldMatrix, 0, 3 ), GetMatrixData( WorldMatrix, 1, 3 ), GetMatrixData( WorldMatrix, 2, 3 ) ) );

				Out.Normal = normalize( mul( CastTo3x3( WorldMatrix ), Input.Normal ) );
				Out.Tangent = normalize( mul( CastTo3x3( WorldMatrix ), Input.Tangent ) );
				Out.Bitangent = normalize( cross( Out.Normal, Out.Tangent ) * Input.Tangent.w );
				Out.Position = mul( WorldMatrix, Position );
				Out.WorldSpacePos = Out.Position.xyz;
				Out.WorldSpacePos /= WorldMatrix[3][3];
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, Out.Position );

				Out.UV0 = Input.UV0;
				Out.UV1 = Input.UV1;

				Out.InstanceIndex = Input.InstanceIndices.y;

				return Out;
			}
		]]
	}
	MainCode VS_sine_animation_shadow
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT_PDXMESHSHADOWSTANDARD"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_PDXMESHSHADOWSTANDARD Out;

				float4 Position = float4( Input.Position.xyz, 1.0 );
				float4x4 WorldMatrix = PdxMeshGetWorldMatrix( Input.InstanceIndices.y );

				// Reset Rotation
				WorldMatrix[0][0] = 1;
				WorldMatrix[0][1] = 0;
				WorldMatrix[0][2] = 0;
				WorldMatrix[1][0] = 0;
				WorldMatrix[1][1] = 1;
				WorldMatrix[1][2] = 0;
				WorldMatrix[2][0] = 0;
				WorldMatrix[2][1] = 0;
				WorldMatrix[2][2] = 1;

				// Wave Animation
				CalculateSineAnimation( Input.UV1, Position.xyz, Input.Normal, Input.Tangent, float3( GetMatrixData( WorldMatrix, 3, 0 ), GetMatrixData( WorldMatrix, 3, 1 ), GetMatrixData( WorldMatrix, 3, 2 ) ) );

				Out.Position = mul( WorldMatrix, Position );
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, Out.Position );
				Out.UV_InstanceIndex.xy = Input.UV0;
				Out.UV_InstanceIndex.z = Input.InstanceIndices.y;

				return Out;
			}
		]]
	}

	MainCode VS_sine_animation_mapobject
	{
		Input = "VS_INPUT_PDXMESH_MAPOBJECT"
		Output = "VS_OUTPUT"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT Out;

				float4 Position = float4( Input.Position.xyz, 1.0 );
				float4x4 WorldMatrix = UnpackAndGetMapObjectWorldMatrix( Input.InstanceIndex24_Opacity8 );

				// Reset Rotation
				WorldMatrix[0][0] = 1;
				WorldMatrix[0][1] = 0;
				WorldMatrix[0][2] = 0;
				WorldMatrix[1][0] = 0;
				WorldMatrix[1][1] = 1;
				WorldMatrix[1][2] = 0;
				WorldMatrix[2][0] = 0;
				WorldMatrix[2][1] = 0;
				WorldMatrix[2][2] = 1;

				// Wave animation
				CalculateSineAnimation( Input.UV1, Position.xyz, Input.Normal, Input.Tangent, float3( GetMatrixData( WorldMatrix, 0, 3 ), GetMatrixData( WorldMatrix, 1, 3 ), GetMatrixData( WorldMatrix, 2, 3 ) ) );

				Out.Normal = normalize( mul( CastTo3x3( WorldMatrix ), Input.Normal ) );
				Out.Tangent = normalize( mul( CastTo3x3( WorldMatrix ), Input.Tangent ) );
				Out.Bitangent = normalize( cross( Out.Normal, Out.Tangent ) * Input.Tangent.w );
				Out.Position = mul( WorldMatrix, Position );
				Out.WorldSpacePos = Out.Position.xyz;
				Out.WorldSpacePos /= WorldMatrix[3][3];
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, Out.Position );

				Out.UV0 = Input.UV0;
				Out.UV1 = Input.UV1;

				Out.InstanceIndex = Input.InstanceIndex24_Opacity8;

				return Out;
			}
		]]
	}
	MainCode VS_sine_animation_shadow_mapobject
	{
		Input = "VS_INPUT_PDXMESH_MAPOBJECT"
		Output = "VS_OUTPUT_MAPOBJECT_SHADOW"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_MAPOBJECT_SHADOW Out;

				float4 Position = float4( Input.Position.xyz, 1.0 );
				float4x4 WorldMatrix = UnpackAndGetMapObjectWorldMatrix( Input.InstanceIndex24_Opacity8 );

				// Reset Rotation
				WorldMatrix[0][0] = 1;
				WorldMatrix[0][1] = 0;
				WorldMatrix[0][2] = 0;
				WorldMatrix[1][0] = 0;
				WorldMatrix[1][1] = 1;
				WorldMatrix[1][2] = 0;
				WorldMatrix[2][0] = 0;
				WorldMatrix[2][1] = 0;
				WorldMatrix[2][2] = 1;

				// Wave Animation
				CalculateSineAnimation( Input.UV1, Position.xyz, Input.Normal, Input.Tangent, float3( GetMatrixData( WorldMatrix, 3, 0 ), GetMatrixData( WorldMatrix, 3, 1 ), GetMatrixData( WorldMatrix, 3, 2 ) ) );

				Out.Position = mul( WorldMatrix, Position );
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, Out.Position );
				Out.InstanceIndex24_Opacity8 = Input.InstanceIndex24_Opacity8;

				return Out;
			}
		]]
	}
}


PixelShader =
{
	Code
	[[
		float ApplyOpacity( float BaseAlpha, float2 NoiseCoordinate, in uint InstanceIndex )
		{
		#ifdef JOMINI_MAP_OBJECT
			float Opacity = UnpackAndGetMapObjectOpacity( InstanceIndex );
		#else
			float Opacity = PdxMeshGetOpacity( InstanceIndex );
		#endif
			return PdxMeshApplyOpacity( BaseAlpha, NoiseCoordinate, Opacity );
		}
	]]
	MainCode PS_standard
	{
		Input = "VS_OUTPUT"
		Output = "PS_COLOR_SSAO"
		Code
		[[
			#define DIFFUSE_UV_SET Input.UV0
			#define NORMAL_UV_SET Input.UV0
			#define PROPERTIES_UV_SET Input.UV0
			#define UNIQUE_UV_SET Input.UV1

			PDX_MAIN
			{
				PS_COLOR_SSAO Out;

				#ifdef UNDERWATER
					clip( _WaterHeight - Input.WorldSpacePos.y + 0.1 ); // +0.1 to avoid gap between water and mesh
				#endif

				float2 MapCoords = Input.WorldSpacePos.xz * _WorldSpaceToTerrain0To1;
				float2 ProvinceCoords = Input.WorldSpacePos.xz / _ProvinceMapSize;
				float LocalHeight = Input.WorldSpacePos.y - GetHeight( Input.WorldSpacePos.xz );

				float4 Diffuse = PdxTex2D( DiffuseMap, DIFFUSE_UV_SET );
				float4 Properties = PdxTex2D( PropertiesMap, PROPERTIES_UV_SET );

				// Alpha
				Diffuse.a = ApplyOpacity( Diffuse.a, Input.Position.xy, Input.InstanceIndex );
				#ifdef ALPHA_TO_COVERAGE
					Diffuse.a = RescaleAlphaByMipLevel( Diffuse.a, DIFFUSE_UV_SET, DiffuseMap );
					Diffuse.a = SharpenAlpha( Diffuse.a, 0.5f );
				#endif
				clip( Diffuse.a - 0.001f );

				// Normal calculation
				float4 NormalSample = PdxTex2D( NormalMap, NORMAL_UV_SET );
				float3 InNormal = normalize( Input.Normal );
				float3x3 TBN = Create3x3( normalize( Input.Tangent ), normalize( Input.Bitangent ), InNormal );
				float3 Normal = normalize( mul( UnpackRRxGNormal( NormalSample ), TBN ) );

				// Devastation
				ApplyDevastationBuilding( Diffuse.rgb, Input.WorldSpacePos.xz, LocalHeight, DIFFUSE_UV_SET );

				// Revolution flag
				#ifdef REVOLUTIONFLAG
						#if defined( IG_USERDATA )
							uint InterestGroupColorIndex = GetUserDataUint( Input.InstanceIndex );
							float4 InterestGroupColor = GetInterestGroupColorUserdata( InterestGroupColorIndex );
						#else
							float4 InterestGroupColor = GetInterestGroupColorDefine();
						#endif
					Diffuse.rgb = Overlay( Diffuse.rgb, ToLinear( HSVtoRGB( InterestGroupColor.rgb ) ) );
				#endif

				// Baked AO
				#if defined( TINT_COLOR )
					float4 Unique = PdxTex2D( TintMap, UNIQUE_UV_SET );
					Diffuse.rgb = Overlay( Diffuse.rgb, Unique.rgb );
				#endif

				// Bottom tint effetc
				float TintAngleModifier = saturate( 1.0 - dot( InNormal, float3( 0.0, 1.0, 0.0 ) ) );	// Removes tint from angles facing upwards
				float TintBlend = ( 1.0 - smoothstep( _MeshTintHeightMin, _MeshTintHeightMax, LocalHeight ) ) * _MeshTintColor.a * TintAngleModifier;
				Diffuse.rgb = lerp(  Diffuse.rgb, Overlay( Diffuse.rgb, _MeshTintColor.rgb ), TintBlend );

				// Colormap blend, pre light
				#if defined( COLORMAP )
					float3 ColorMap = PdxTex2D( ColorTexture, float2( MapCoords.x, 1.0 - MapCoords.y ) ).rgb;
					Diffuse.rgb = SoftLight( Diffuse.rgb, ColorMap, ( 1 - Properties.r ) );
				#endif

				// Color overlay, pre light
				#ifndef UNDERWATER
					#ifndef NO_BORDERS
						float3 ColorOverlay;
						float PreLightingBlend;
						float PostLightingBlend;
						GameProvinceOverlayAndBlend( ProvinceCoords, Input.WorldSpacePos, ColorOverlay, PreLightingBlend, PostLightingBlend );
						Diffuse.rgb = ApplyColorOverlay( Diffuse.rgb, ColorOverlay, PreLightingBlend );
					#endif
				#endif

				// Light and shadow
				float3 Color = Diffuse.rgb;
				Properties.a = ScaleRoughnessByDistance( Properties.a, Input.WorldSpacePos );
				SMaterialProperties MaterialProps = GetMaterialProperties( Diffuse.rgb, Normal, Properties.a, Properties.g, Properties.b );
				SLightingProperties LightingProps = GetSunLightingProperties( Input.WorldSpacePos, ShadowMap );
				#ifndef LOW_QUALITY_SHADERS
					#ifndef FLATLIGHT
						Color = CalculateSunLighting( MaterialProps, LightingProps, EnvironmentMap );

						// Second sun
						#ifndef SINGLESUN
							SLightingProperties SecondLightingProps = GetSecondSunLightingProperties( Input.WorldSpacePos );
							float3 SecondSunColor = CalculateSecondSunLighting( MaterialProps, SecondLightingProps );
							Color += SecondSunColor;
						#endif
					#endif
				#endif
				#if defined( EMISSIVE_NIGHT ) || defined( EMISSIVE_NIGHT_RANDOM )
						float ActivationThreshold = 0.05;
						float ShouldActivate = 1.0;
						float4 LightColor = _NightLightColor;

						#if defined( HUB_BUILDING )
							ActivationThreshold = GetUserDataRandomValueCity( Input.InstanceIndex );
							#if defined( EMISSIVE_NIGHT_RANDOM )
								ShouldActivate = clamp( GetUserDataShouldLightActivate( Input.InstanceIndex ), 0.0f, 1.0f );
							#endif
							LightColor = GetUserDataBuildingLightColor( Input.InstanceIndex );
						#endif

						float DayNightModifier = Remap( _DayNightValue, _LightsActivateBegin, _LightsActivateEnd, 0.0, 1.0 );
						float LightValue = saturate( Remap( DayNightModifier, ActivationThreshold, _LightsFadeTime + ActivationThreshold, 0.0, 1.0 ) );
						if ( DayNightModifier > ActivationThreshold )
						{
							Color += NormalSample.b * LightColor.rgb * LightColor.a * LightValue * ShouldActivate;
						}
				#endif

				// Effects, post light
				#ifndef UNDERWATER
					#ifndef NO_BORDERS
						Color = ApplyColorOverlay( Color, ColorOverlay, PostLightingBlend );
					#endif
					#ifndef NO_FOG
						if( _FlatmapLerp < 1.0 )
						{
							float3 Unfogged = Color;
							Color = ApplyFogOfWar( Color, Input.WorldSpacePos );
							Color = GameApplyDistanceFog( Color, Input.WorldSpacePos );
							Color = lerp( Color, Unfogged, _FlatmapLerp );
						}
					#endif
				#endif

				// Refraction
				#ifdef UNDERWATER
					Diffuse.a = CompressWorldSpace( Input.WorldSpacePos );
				#endif

				// Province Highlight
				Color = ApplyHighlight( Color, ProvinceCoords );

				// Flatmap
				#ifdef FLATMAP
				 	float LandMask = PdxTex2DLod0( LandMaskMap, float2( MapCoords.x, 1.0 - MapCoords.y ) ).r;
					Diffuse.a *= ( 1.0 - ( LandMask * ( 1.0 - _FlatmapOverlayLandOpacity ) ) );
				#endif

				// Debug
				DebugReturn( Color, MaterialProps, LightingProps, EnvironmentMap );

				// Output
				Out.Color = float4( Color, Diffuse.a );
				float3 SSAOColor_ = _SSAOColorMesh.rgb + GameCalculateDistanceFogFactor( Input.WorldSpacePos );
				#ifndef UNDERWATER
					#ifndef NO_BORDERS
						SSAOColor_ = SSAOColor_ + PostLightingBlend;
					#endif
				#endif
				Out.SSAOColor = float4( saturate ( SSAOColor_ ), Diffuse.a);

				return Out;
			}
		]]
	}
}


BlendState BlendState
{
	BlendEnable = no
}
BlendState alpha_blend
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}
BlendState alpha_to_coverage
{
	BlendEnable = no
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
	AlphaToCoverage = yes
}

DepthStencilState depth_test_no_write
{
	DepthEnable = yes
	DepthWriteEnable = no
}

RasterizerState RasterizerState
{
	DepthBias = 0
	SlopeScaleDepthBias = 0
}
RasterizerState ShadowRasterizerState
{
	DepthBias = 0
	SlopeScaleDepthBias = 2
}
RasterizerState FlatmapRasterizerState
{
	DepthBias = -500
	SlopeScaleDepthBias = -7
}

# Standard
Effect standard
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
}
Effect standardShadow
{
	VertexShader = "VS_standard_shadow"
	PixelShader = "PixelPdxMeshStandardShadow"
	RasterizerState = ShadowRasterizerState
}

# Standard + alpha blend
Effect standard_alpha_blend
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
	BlendState = "alpha_blend"
	DepthStencilState = "depth_test_no_write"
}
Effect standard_alpha_blendShadow
{
	VertexShader = "VS_standard_shadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
}

# Standard + a2c
Effect standard_alpha_to_coverage
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
	BlendState = "alpha_to_coverage"
	Defines = { "ALPHA_TO_COVERAGE" }
}
Effect standard_alpha_to_coverageShadow
{
	VertexShader = "VS_standard_shadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	RasterizerState = ShadowRasterizerState
	Defines = { "ALPHA_TO_COVERAGE" }
}

# Flag animation
Effect standard_flag_basic
{
	VertexShader = "VS_sine_animation"
	PixelShader = "PS_standard"
}
Effect standard_flag_basicShadow
{
	VertexShader = "VS_sine_animation_shadow"
	PixelShader = "PixelPdxMeshStandardShadow"
	RasterizerState = ShadowRasterizerState
}
Effect standard_flag_revolution
{
	VertexShader = "VS_sine_animation"
	PixelShader = "PS_standard"

	Defines = { "REVOLUTIONFLAG" "IG_USERDATA" }
}
Effect standard_flag_revolutionShadow
{
	VertexShader = "VS_sine_animation_shadow"
	PixelShader = "PixelPdxMeshStandardShadow"
	RasterizerState = ShadowRasterizerState
}


# Flatmap
Effect flatmap_alpha_blend_no_borders
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
	BlendState = "alpha_blend"
	DepthStencilState = "depth_test_no_write"
	RasterizerState = FlatmapRasterizerState
	Defines = { "NO_BORDERS" "NO_FOG"  }
}
Effect flatmap_alpha_blend_no_bordersShadow
{
	VertexShader = "VS_standard_shadow"
	PixelShader = "PixelPdxMeshAlphaBlendShadow"
	Defines = { "NO_FOG" }
	RasterizerState = ShadowRasterizerState
}

# Extra
Effect material_test
{
	VertexShader = "VS_standard"
	PixelShader = "PS_standard"
	Defines = { "NORMAL_UV_SET Input.UV1" "DIFFUSE_UV_SET Input.UV1" }
}


############################
# Map object shaders

# Standard
Effect standard_mapobject
{
	VertexShader = "VS_mapobject"
	PixelShader = "PS_standard"
}
Effect standardShadow_mapobject
{
	VertexShader = "VS_jomini_mapobject_shadow"
	PixelShader = "PS_jomini_mapobject_shadow"
	RasterizerState = ShadowRasterizerState
}

# Standard + alpha blend
Effect standard_alpha_blend_mapobject
{
	VertexShader = "VS_mapobject"
	PixelShader = "PS_standard"
	BlendState = "alpha_blend"
	DepthStencilState = "depth_test_no_write"
}
Effect standard_alpha_blendShadow_mapobject
{
	VertexShader = "VS_jomini_mapobject_shadow"
	PixelShader = "PS_jomini_mapobject_shadow_alphablend"
	RasterizerState = ShadowRasterizerState
}

# Standard + a2c
Effect standard_alpha_to_coverage_mapobject
{
	VertexShader = "VS_mapobject"
	PixelShader = "PS_standard"
	BlendState = "alpha_to_coverage"
	Defines = { "ALPHA_TO_COVERAGE" }
}
Effect standard_alpha_to_coverageShadow_mapobject
{
	VertexShader = "VS_jomini_mapobject_shadow"
	PixelShader = "PS_jomini_mapobject_shadow_alphablend"
	RasterizerState = ShadowRasterizerState
	Defines = { "ALPHA_TO_COVERAGE" }
}

# Flag animation
Effect standard_flag_basic_mapobject
{
	VertexShader = "VS_sine_animation_mapobject"
	PixelShader = "PS_standard"
}
Effect standard_flag_basicShadow_mapobject
{
	VertexShader = "VS_sine_animation_shadow_mapobject"
	PixelShader = "PS_jomini_mapobject_shadow"
	RasterizerState = ShadowRasterizerState
}
Effect standard_flag_revolution_mapobject
{
	VertexShader = "VS_sine_animation_mapobject"
	PixelShader = "PS_standard"

	Defines = { "REVOLUTIONFLAG" "IG_USERDATA" }
}
Effect standard_flag_revolutionShadow_mapobject
{
	VertexShader = "VS_sine_animation_shadow_mapobject"
	PixelShader = "PS_jomini_mapobject_shadow"
	RasterizerState = ShadowRasterizerState
}

# Flatmap
Effect flatmap_alpha_blend_no_borders_mapobject
{
	VertexShader = "VS_mapobject"
	PixelShader = "PS_standard"
	BlendState = "alpha_blend"
	DepthStencilState = "depth_test_no_write"
	RasterizerState = FlatmapRasterizerState
	Defines = { "NO_BORDERS" "NO_FOG" "FLATMAP"  }
}
Effect flatmap_alpha_blend_no_bordersShadow_mapobject
{
	VertexShader = "VS_jomini_mapobject_shadow"
	PixelShader = "PS_jomini_mapobject_shadow_alphablend"
	Defines = { "NO_FOG" "FLATMAP" }
	RasterizerState = ShadowRasterizerState
}
