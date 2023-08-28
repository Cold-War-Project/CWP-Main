Includes = {
	"sharedconstants.fxh"
	"jomini/countrynames.fxh"
	"distance_fog.fxh"
	"fog_of_war.fxh"
}

VertexShader =
{
	MainCode MapNameVertexShader
	{
		Input = "VS_INPUT_MAPNAME"
		Output = "VS_OUTPUT_MAPNAME"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_MAPNAME Out = MapNameVertexShader( Input, _FlatmapHeight, _FlatmapLerp );
				return Out;
			}
		]]
	}
}

PixelShader =
{
	TextureSampler FontAtlas
	{
		Ref = PdxTexture0
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}

	MainCode MapNamePixelShader
	{
		Input = "VS_OUTPUT_MAPNAME"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float Alpha = CalcAlphaDistanceField( FontAtlas, Input.TexCoord );
				float3 Color = lerp( 1.0f, 1.0f, 1.0f );
				
				float3 FlatmapColor = Color; // Pre effects color

				// Fog of war
				Color = ApplyFogOfWar( Color, Input.WorldSpacePos );

				// Flatmap color
				Color = lerp( Color, FlatmapColor, _FlatmapLerp);

				return float4( Color, Alpha );
			}
		]]
	}
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
	WriteMask = "RED|GREEN|BLUE"
}

RasterizerState RasterizerState
{
	frontccw = yes
}

DepthStencilState DepthStencilState
{
	DepthEnable = no
}


Effect mapname
{
	VertexShader = "MapNameVertexShader"
	PixelShader = "MapNamePixelShader"
}

