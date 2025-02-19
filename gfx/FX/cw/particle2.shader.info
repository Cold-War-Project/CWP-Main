Includes = {
	"cw/particle2.fxh"
	"distance_fog.fxh"
	"cwp_coloroverlay.fxh"
	"fog_of_war.fxh"
	"ssao_struct.fxh"
}

PixelShader =
{
	MainCode PixelTexture
	{
		Input = "VS_OUTPUT_PARTICLE"
		Output = "PS_COLOR_SSAO"
		Code
		[[
			PDX_MAIN
			{
				PS_COLOR_SSAO Out;
				float4 Color = PdxTex2D( DiffuseMap, Input.UV0 ) * Input.Color;
				float2 ProvinceCoords = Input.WorldSpacePos.xz / _ProvinceMapSize;

				float3 OverlayColor = Color.rgb;
				OverlayColor = ApplyFogOfWar( OverlayColor, Input.WorldSpacePos );
				OverlayColor = GameApplyDistanceFog( OverlayColor, Input.WorldSpacePos );
				Color.rgb = lerp( Color.rgb, OverlayColor, 1.0 - _FlatmapLerp );

				// Output
				Out.Color = Color;

				return Out;
			}
		]]
	}
}

RasterizerState RasterizerStateNoCulling
{
	CullMode = "none"
}

DepthStencilState DepthStencilState
{
	DepthEnable = yes
	DepthWriteEnable = no
}

BlendState BlendState
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
	WriteMask = "RED|GREEN|BLUE"
}

Effect ParticleTexture
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelTexture"
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleColor
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelColor"
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleTextureBillboard
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelTexture"
	Defines = { "BILLBOARD" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleColorBillboard
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelColor"
	Defines = { "BILLBOARD" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleTBE
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelTexture"
	BlendState = "AdditiveBlendState"
	Defines = { "BILLBOARD" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleCBE
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelColor"
	BlendState = "AdditiveBlendState"
	Defines = { "BILLBOARD" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleTE
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelTexture"
	BlendState = "AdditiveBlendState"
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleCE
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelColor"
	BlendState = "AdditiveBlendState"
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleColorFade
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelColor"
	Defines = { "FADE_STEEP_ANGLES" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleTextureFade
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelTexture"
	Defines = { "FADE_STEEP_ANGLES" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleCFE
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelColor"
	BlendState = "AdditiveBlendState"
	Defines = { "FADE_STEEP_ANGLES" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleTFE
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelTexture"
	BlendState = "AdditiveBlendState"
	Defines = { "FADE_STEEP_ANGLES" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleCFB
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelColor"
	Defines = { "FADE_STEEP_ANGLES" "BILLBOARD" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleTFB
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelTexture"
	Defines = { "FADE_STEEP_ANGLES" "BILLBOARD" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleCFBE
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelColor"
	BlendState = "AdditiveBlendState"
	Defines = { "FADE_STEEP_ANGLES" "BILLBOARD" }
	RasterizerState = "RasterizerStateNoCulling"
}

Effect ParticleTFBE
{
	VertexShader = "VertexParticle"
	PixelShader = "PixelTexture"
	BlendState = "AdditiveBlendState"
	Defines = { "FADE_STEEP_ANGLES" "BILLBOARD" }
	RasterizerState = "RasterizerStateNoCulling"
}
