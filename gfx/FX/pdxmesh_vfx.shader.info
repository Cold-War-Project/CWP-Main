Includes = {
	"cw/camera.fxh"
	"cw/pdxmesh.fxh"

	"pdxmesh_vfx.fxh"
	"coloroverlay.fxh"
	"ssao_struct.fxh"
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
		srgb = yes
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
	uint InstanceIndex 		: TEXCOORD6;
	float2 UV2				: TEXCOORD7;
};

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
			Out.UV2 = In.UV1;
			Out.WorldSpacePos = In.WorldSpacePos;
			return Out;
		}

		void BillboardMVPMatrix ( inout float4x4 MVPMatrix, in int3 BillboardAxis )
		{
			if(!BillboardAxis.x)
			{
				MVPMatrix[0][0] = 1.0f;
				MVPMatrix[0][1] = 0.0f;
				MVPMatrix[0][2] = 0.0f;
			}

			if(!BillboardAxis.y)
			{
				MVPMatrix[1][0] = 0.0f;
				MVPMatrix[1][1] = 1.0f;
				MVPMatrix[1][2] = 0.0f;
			}

			if(!BillboardAxis.z)
			{
				MVPMatrix[2][0] = 0.0f;
				MVPMatrix[2][1] = 0.0f;
				MVPMatrix[2][2] = 1.0f;
			}
		}

		void ApplyJointAnimation (
			inout VS_OUTPUT Out,
			in VS_INPUT_PDXMESHSTANDARD Input,
			in float4x4 WorldMatrix)
		{
			#ifdef PDX_MESH_SKINNED
				float4 Position = float4( Input.Position.xyz, 1.0 );
				float3 BaseNormal = Input.Normal;
				float3 BaseTangent = Input.Tangent.xyz;

				float4 SkinnedPosition = vec4( 0.0 );
				float3 SkinnedNormal = vec3( 0.0 );
				float3 SkinnedTangent = vec3( 0.0 );
				float3 SkinnedBitangent = vec3( 0.0 );

				uint JointsInstanceIndex = Input.InstanceIndices.x;

				float4 Weights = float4( Input.BoneWeight.xyz, 1.0 - Input.BoneWeight.x - Input.BoneWeight.y - Input.BoneWeight.z );

				for( int i = 0; i < PDXMESH_MAX_INFLUENCE; ++i )
				{
					uint BoneIndex = Input.BoneIndex[i];
					uint OffsetIndex = BoneIndex + JointsInstanceIndex;

					float4x4 VertexMatrix = PdxMeshGetJointVertexMatrix( OffsetIndex );
					float3x3 VertexRotationMatrix = CastTo3x3( VertexMatrix );
					float3x3 NormalMatrix = transpose( VertexRotationMatrix );

					SkinnedPosition += mul( VertexMatrix, Position ) * Weights[ i ];

					// TODO [FM]: PSGE-3819 Better skinned normals
					float3 Normal = mul( NormalMatrix, BaseNormal );
					float3 Tangent = mul( NormalMatrix, BaseTangent );
					float3 Bitangent = cross( Normal, Tangent ) * Input.Tangent.w;
					Bitangent = normalize( Bitangent );

					SkinnedNormal += Normal * Weights[i];
					SkinnedTangent += Tangent * Weights[i];
					SkinnedBitangent += Bitangent * Weights[i];
				}

				Out.Normal = normalize( mul( CastTo3x3( WorldMatrix ), normalize( SkinnedNormal ) ) );
				Out.Tangent = normalize( mul( CastTo3x3( WorldMatrix ), normalize( SkinnedTangent ) ) );
				Out.Bitangent = normalize( mul( CastTo3x3( WorldMatrix ), normalize( SkinnedBitangent ) ) );

				Out.Position = SkinnedPosition;
			#endif
		}

	]]

	MainCode VS_mesh_vfx_standard
	{
		Input = "VS_INPUT_PDXMESHSTANDARD"
		Output = "VS_OUTPUT"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT Out = ConvertOutput( PdxMeshVertexShaderStandard( Input ) );
				Out.InstanceIndex = Input.InstanceIndices.y;

				#ifdef BILLBOARD_MESH_SKINNED
					float4x4 WorldMatrix = PdxMeshGetWorldMatrix( Input.InstanceIndices.y );
					float4x4 ProjectionWorldViewMatrix = mul ( ProjectionMatrix, mul ( ViewMatrix, WorldMatrix ) );

					ApplyJointAnimation ( Out, Input, WorldMatrix );
					BillboardMVPMatrix( ProjectionWorldViewMatrix, int3(0, 0, 1) );
					Out.Position = mul( ProjectionWorldViewMatrix, Out.Position );
				#endif

				#ifdef BILLBOARD_MESH
					float4x4 WorldMatrix = PdxMeshGetWorldMatrix( Input.InstanceIndices.y );
					float3 WorldSpacePos = mul( WorldMatrix, float4( float3( 0.0f, 0.0f, 0.0f ), 1.0f ) ).xyz;

					float3 ViewDir = CameraPosition - WorldSpacePos;
					float Angle = atan2( ViewDir.x, ViewDir.z );
					float Cosine = cos( Angle );
					float Sine = sin( Angle );
					float3x3 RotMarix = Create3x3( float3( Cosine, 0, Sine ), float3( 0, 1.0, 0 ), float3( -Sine, 0.0, Cosine ) );

					float4 NewPos = float4( mul( RotMarix, Input.Position.xyz ), 1.0 );
					NewPos = mul( WorldMatrix, NewPos );
					Out.Position = FixProjectionAndMul( ViewProjectionMatrix, NewPos );
				#endif

				#ifdef UI_PANNING_TEXTURE
					Out.UV1 = Input.UV0;

					Out.UV0 *= UI_PANNING_TEXTURE_UV0_MULT;
					Out.UV0  = frac ( GlobalTime * UI_PANNING_TEXTURE_UV2_SPEED );

					Out.UV2 *= UI_PANNING_TEXTURE_UV2_MULT;
					Out.UV2 += frac( GlobalTime * UI_PANNING_TEXTURE_UV2_SPEED );
				#endif

				#ifdef UI_SCREEN_BURN
					Out.UV0 *= UI_SCREEN_BURN_UV0_MULT;
					Out.UV1 = Out.UV0;

					Out.UV0 += vec2(frac(GlobalTime * UI_SCREEN_BURN_UV0_SPEED));
					Out.UV1 += vec2(frac(GlobalTime * UI_SCREEN_BURN_UV1_SPEED));
				#endif

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
	MainCode PS_mesh_vfx_standard
	{
		Input = "VS_OUTPUT"
		Output = "PS_COLOR_SSAO"
		Code
		[[
			PDX_MAIN
			{
				PS_COLOR_SSAO Out;

				#ifdef SIMPLE_UNLIT_DIFFUSE
					Out.Color.rgb = PdxTex2D( DiffuseMap, Input.UV0 ).rgb;
					Out.Color.a = 1.0f;
				#endif

				#ifdef UI_PANNING_TEXTURE
					// Mask for the lower edge
					float LowerEdgeMask = saturate( ( Input.UV1.y - LOWER_EDGE_FALLOFF ) );
					float4 NoiseTextureSample = PdxTex2D( DiffuseMap, Input.UV1.xy );

					// Distorted and Base UV Sets used to sample textures later
					float2 BaseUV = float2( Input.UV2.x, Input.UV2.y );
					float2 DistortedUVs = BaseUV + float2( NoiseTextureSample.r, NoiseTextureSample.g ) * UV_DIST_STRENGTH;

					float4 NoiseTexture;
					float4 NoiseTextureDistorted2 = PdxTex2D( DiffuseMap, DistortedUVs );

					NoiseTexture = NoiseTextureSample * NoiseTextureDistorted2;

					// Texture Masks for the Upper and Lower Edge
					float UpperEdge = saturate( ( ( saturate( 1.0f - Input.UV1.y + NoiseTexture.a ) ) + UPPER_EDGE_FALLOFF ) );
					float LowerEdge = LowerEdgeMask + ( LowerEdgeMask * NoiseTexture.a ) * LOWER_EDGE_MULT;
					float LowerEdge2 = LowerEdgeMask + ( LowerEdgeMask * NoiseTexture.g ) * LOWER_EDGE_MULT;

					// Final Composite RGB
					float4 Composite;

					float LowerCut = smoothstep( 0.0f, LOWER_EDGE_CUT, LowerEdge * LowerEdge2 );

					Composite.rgb = lerp( NoiseTexture.a, NoiseTexture.r, LowerEdge ) + LowerEdge;
					Composite.rgb = PdxTex2D( PropertiesMap, saturate( float2( Composite.r + LOWER_EDGE_COL_SLIDE, Composite.g ) ) ).rgb;
					Composite.rgb = lerp(Composite.rgb, UPPER_EDGE_COL, UpperEdge );

					// Final Composite Alpha
					Composite.a = saturate( LowerEdgeMask + Input.UV1.g * NoiseTextureDistorted2.a * FINAL_ALPHA_MULT );
					Composite.a = saturate( Composite.a - LowerCut );
					Composite.a*= NoiseTextureSample.b;

					Out.Color = Composite;
					Out.Color.rgb *= FINAL_COL_MULT;
					Out.Color.a *= PdxMeshGetOpacity(Input.InstanceIndex);

				#endif

				#ifdef UI_SCREEN_BURN
					float4 UVDistortion = ( PdxTex2D( DiffuseMap, Input.UV1 ) + 1.0f ) * 0.5f;
					float UVDistortionStrength = 0.1f;

					Out.Color = PdxTex2D( DiffuseMap, Input.UV0 + UVDistortion.zw * UVDistortionStrength );

					float a = ( sin( GlobalTime * 2.0f ) + 1.0f ) * 0.5f;

					float Alpha = smoothstep( a, saturate( a - 0.025f ), 1.0f - Out.Color.a );
					float Alpha2 = Alpha - smoothstep( a, saturate( a - 0.05f), 1.0f - Out.Color.a );

					Out.Color.a = Alpha;
					Out.Color.rgb = lerp( float3( 0.0f, 0.0f, 0.0f ), float3( 0.0f, 0.0f, 0.0f ), a * a * a ) + Alpha2 * float3( 3.0f, 0.0f, 0.0f );
					Out.Color.a = ApplyOpacity( Out.Color.a, Input.Position.xy, Input.InstanceIndex );
				#endif

				return Out;
			}
		]]
	}

	MainCode PS_mesh_vfx_candle
	{
		Input = "VS_OUTPUT"
		Output = "PS_COLOR_SSAO"
		Code
		[[
			PDX_MAIN
			{
				PS_COLOR_SSAO Out;

				float2 NoiseUv = Input.UV0;
				float2 PanSpeed = float2( 0.125, 0.055 );
				float NoiseStrength = 0.15f;
				float DistortionStrength = 0.2f;

				NoiseUv *= NoiseStrength;
				NoiseUv += GlobalTime * PanSpeed;

				float2 NormalNoise = PdxTex2D( NormalMap, NoiseUv ).rg;
				NormalNoise -= 0.5;
				NormalNoise *= DistortionStrength;

				float VerticalGradient = smoothstep( 1.0f, 0.0f, Input.UV0.y );
				float2 UvDistortion = lerp( float2( 0.0f, 0.0f ), NormalNoise, VerticalGradient );
				float4 Diffuse = PdxTex2D( DiffuseMap, Input.UV0 + UvDistortion );
				Diffuse.a = ApplyOpacity( Diffuse.a, Input.Position.xy, Input.InstanceIndex );

				clip( Diffuse.a - 0.1f );

				Out.Color = Diffuse;
				Out.SSAOColor = float4( 1.0f, 1.0f, 1.0f, Diffuse.a );
				return Out;
			}
		]]
	}

}

RasterizerState RasterizerStateNoCulling
{
	CullMode = "none"
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
	WriteMask = "RED|GREEN|BLUE"
}

BlendState AdditiveBlendState
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "ONE"
	WriteMask = "RED|GREEN|BLUE|ALPHA"
}


BlendState additive_blend
{
	BlendEnable = yes
	SourceBlend = "ONE"
	DestBlend = "ONE"

}

DepthStencilState depth_test_no_write
{
	DepthEnable = yes
	DepthWriteEnable = no
}

# Standard
Effect mesh_vfx_standard
{
	VertexShader = "VS_mesh_vfx_standard"
	PixelShader = "PS_mesh_vfx_standard"
}

# Standard + candle distortion
Effect mesh_vfx_candle
{
	VertexShader = "VS_mesh_vfx_standard"
	PixelShader = "PS_mesh_vfx_candle"
	BlendState = "alpha_blend"
	Defines = { "BILLBOARD_MESH" }
}

# Standard
Effect mesh_vfx_standard_billboard
{
	VertexShader = "VS_mesh_vfx_standard"
	PixelShader = "PS_mesh_vfx_standard"
	Defines = { "BILLBOARD_MESH_SKINNED" "SIMPLE_UNLIT_DIFFUSE" }
}

# Standard + alpha blend
Effect standard_alpha_blend
{
	VertexShader = "VS_mesh_vfx_standard"
	PixelShader = "PS_mesh_vfx_standard"
	BlendState = "alpha_blend"
	DepthStencilState = "depth_test_no_write"
}

# Standard + alpha blend, used for panning textures on UI quads
Effect vfx_ui_panning_texture
{
	VertexShader = "VS_mesh_vfx_standard"
	PixelShader = "PS_mesh_vfx_standard"
	BlendState = "alpha_blend"
	DepthStencilState = "depth_test_no_write"
	Defines = { "UI_PANNING_TEXTURE" }
}

# Standard + alpha blend, used for dissolving textures on UI quads
Effect vfx_ui_screen_burn
{
	VertexShader = "VS_mesh_vfx_standard"
	PixelShader = "PS_mesh_vfx_standard"
	BlendState = "alpha_blend"
	DepthStencilState = "depth_test_no_write"
	Defines = { "UI_SCREEN_BURN" }
}

# Standard + additive blend
Effect standard_additive_blend
{
	VertexShader = "VS_mesh_vfx_standard"
	PixelShader = "PS_mesh_vfx_standard"
	BlendState = "additive_blend"
	DepthStencilState = "depth_test_no_write"
}
