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
				
				float DayNightModifier = smoothstep( 0.3, 0.35, _DayNightValue );
				float3 Color = lerp( vec3( 0.0 ), vec3( 0.75 ), DayNightModifier * ( 1.0 - _FlatmapLerp ) );
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

