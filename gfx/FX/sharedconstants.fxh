Includes = {
	"cw/utility.fxh"
	"cw/camera.fxh"
	"cw/lighting.fxh"
	"cw/lighting_util.fxh"
	"cw/pdxterrain.fxh"
}

ConstantBuffer( GameSharedConstants )
{
	float2 MapSize;
	float2 ProvinceMapSize;

	float4 SSAOColorMesh;
	float4 MeshTintColor;
	float4 DecentralizedCountryColor;
	float4 ImpassableTerrainColor;

	float3 _SecondSunDiffuse;
	float _SecondSunIntensity
	float3 _SecondSunDir;

	float GlobalTime;
	float FlatMapHeight;
	float FlatMapLerp;

	float ShorelineMaskBlur;
	float ShorelineExtentStr;
	float ShorelineAlpha;
	int	  ShoreLinesUVScale;

	int ImpassableTerrainTiling
	float ImpassableTerrainHeight
	float DistanceFadeStart
	float DistanceFadeEnd

	float WaterShadowMultiplier;

	float MeshTintHeightMin;
	float MeshTintHeightMax;
	float SSAOAlphaTrees;
	float SSAOAlphaTerrain;

	float FogCloseOffset;
	float FogFarOffset;
	float FogWidthScale;

	float DistanceRoughnessPosition;
	float DistanceRoughnessBlend;
	float DistanceRoughnessScale;
	
	float _OverlayOpacity;

	int _MapPaintingTextureTiling;
	int _MapPaintingFlatmapTextureTiling;
	bool _UseMapmodeTextures;
	bool _UsePrimaryRedAsGradient;
};

PixelShader =
{
	Code
	[[
		float3 GameCalculateSunLighting( SMaterialProperties MaterialProps, SLightingProperties LightingProps  )
		{
			float3 DiffuseLight = vec3( 0.0f );
			float3 SpecularLight = vec3( 0.0f );

			// Light vectors
			float3 H = normalize( LightingProps._ToCameraDir + LightingProps._ToLightDir );
			float NdotV = abs( dot( MaterialProps._Normal, LightingProps._ToCameraDir ) ) + 1e-5;		// Add small values to avoid values of 0
			float NdotL = saturate( dot( MaterialProps._Normal, LightingProps._ToLightDir ) + 1e-5 );
			float NdotH = saturate( dot( MaterialProps._Normal, H ) + 1e-5 );
			float LdotH = saturate( dot( LightingProps._ToLightDir, H ) + 1e-5 );
			float3 LightIntensity = LightingProps._LightIntensity * NdotL * LightingProps._ShadowTerm;

			// Sun diffuse light
			float DiffuseBRDF = CalcDiffuseBRDF( NdotV, NdotL, LdotH, MaterialProps._PerceptualRoughness );
			DiffuseLight = DiffuseBRDF * MaterialProps._DiffuseColor * LightIntensity;

			// Sun specular light
			float3 F = F_Schlick( MaterialProps._SpecularColor, vec3( 1.0f ), LdotH );
			float D = D_GGX( NdotH, lerp( 0.03f , 1.0f , MaterialProps._Roughness ) );		// Remap to avoid super small and super bright highlights
			#ifdef PDX_SimpleLighting
				float Vis = V_Optimized( LdotH, MaterialProps._Roughness );
			#else
				float Vis = V_Schlick( NdotL, NdotV, MaterialProps._Roughness );
			#endif
			SpecularLight = D * F * Vis * LightIntensity;

			return DiffuseLight + SpecularLight;
		}

		SLightingProperties GetSecondSunLightingProperties( float3 WorldSpacePos )
		{
			SLightingProperties LightingProps;
			LightingProps._ToCameraDir = normalize( CameraPosition - WorldSpacePos );

			LightingProps._ToLightDir = _SecondSunDir;
			LightingProps._LightIntensity = _SecondSunDiffuse * _SecondSunIntensity;

			// Default these values
			LightingProps._ShadowTerm = 1.0f;
			LightingProps._CubemapIntensity = 0.0f;
			LightingProps._CubemapYRotation = Float4x4Identity();

			return LightingProps;
		}

		float3 CalculateSecondSunLighting( SMaterialProperties MaterialProps, SLightingProperties LightingProps )
		{
			return GameCalculateSunLighting( MaterialProps, LightingProps );
		}
		
		float ScaleRoughnessByDistance( float Roughness, float3 WorldSpacePos )
		{	
			float3 Intersection = CameraPosition - WorldSpacePos;
			float Scalar = Intersection.y;
			float Distance = length( Intersection );

			Roughness = 1.0 - Roughness;
			float ReducedRoughness = 1.0 - RemapClamped( Distance, DistanceRoughnessPosition * Scalar, DistanceRoughnessPosition * Scalar + DistanceRoughnessBlend, Roughness, Roughness * DistanceRoughnessScale );

			return ReducedRoughness;
		}
		
	]]
}
Code
[[
	float4 AlphaBlendAOverB( float4 A, float4 B )
	{
		float Alpha = A.a + B.a * ( 1.0f - A.a );
		float3 Color = A.rgb * A.a + B.rgb * B.a * ( 1.0f - A.a );
		Color /= clamp( Alpha, 0.01f, 1.0f );
		return float4( Color, Alpha );
	}

	// Vertical Rays
	float RayValue( in float2 coord, in float frequency, in float travelRate, in float maxStrength )
	{
		float ny = 2.0f * ( coord.y - 0.5f );
		float ny2 = min( 1.0f, 2.5f - 2.5f * ny * ny );

		float xModifier = 1.0f * ( cos( GlobalTime * travelRate + coord.x * frequency ) - 0.5f );
		float yModifier = sin( coord.y );
		return maxStrength * xModifier * yModifier * ny2;
	}

	float Hash1_2( in float2 x )
	{
		return frac( sin( dot( x, float2( 52.127f, 61.2871f) ) ) * 521.582f );
	}

	float2 Hash2_2( in float2 x )
	{
		return frac( sin( mul( Create2x2( 20.52f, 24.1994f, 70.291f, 80.171f ),  x ) * 492.194 ) );
	}

	float2 Noise2_2( float2 uv )
	{
		float2 f = smoothstep( 0.0f, 1.0f, frac( uv ) );

		float2 uv00 = floor( uv );
		float2 uv01 = uv00 + float2( 0, 1 );
		float2 uv10 = uv00 + float2( 1, 0 );
		float2 uv11 = uv00 + 1.0f;
		float2 v00 = Hash2_2( uv00 );
		float2 v01 = Hash2_2( uv01 );
		float2 v10 = Hash2_2( uv10 );
		float2 v11 = Hash2_2( uv11 );

		float2 v0 = lerp( v00, v01, f.y );
		float2 v1 = lerp ( v10, v11, f.y );
		float2 v = lerp( v0, v1, f.x );

		return v;
	}

	// Rotates point around 0,0
	float2 Rotate( in float2 p, in float deg )
	{
		float s = sin( deg );
		float c = cos( deg );
		p = mul( Create2x2( s, c, -c, s ), p );
		return p;
	}

]]
