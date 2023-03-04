Includes = {
	"cw/fullscreen_vertexshader.fxh"
}

PixelShader = 
{
	TextureSampler IndirectionMap
	{
		Ref = JominiProvinceColorIndirection
		MinFilter = "Point"
		MagFilter = "Point"
		MipFilter = "Point"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}

	TextureSampler ParameterTexture
	{
		Ref = PdxTexture0
		MagFilter = "Point"
		MinFilter = "Point"
		MipFilter = "Point"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler NoiseTexture
	{
		Ref = PdxTexture1
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler ExclusionMaskTexture
	{
		Ref = PdxTexture2
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}

	MainCode PS_create_dynamic_mask
	{
		Input = "VS_OUTPUT_FULLSCREEN"
		Output = "PDX_COLOR"
		Code 
		[[
			float3 GetParameter(float2 UV)
			{
				float2 ColorIndex = PdxTex2DLod0( IndirectionMap, UV ).rg;
				return PdxTex2DLoad0( ParameterTexture, int2( ColorIndex * 255.0 ) ).rgb;
			}

			PDX_MAIN
			{
				float3 ParameterValue = GetParameter(Input.uv);

				float Noise = PdxTex2D(NoiseTexture, Input.uv).r;
				float ExclusionMask = PdxTex2D(ExclusionMaskTexture, Input.uv).r;
				return float4( ParameterValue.r, ParameterValue.g, ExclusionMask , Noise );
			}
		]]
	}
}

BlendState BlendState
{
	BlendEnable = no
}

Effect CreateDynamicMask
{
	VertexShader = VertexShaderFullscreen
	PixelShader = PS_create_dynamic_mask
}