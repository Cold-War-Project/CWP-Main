Includes = {
	"cw/terrain.fxh"
	"cw/utility.fxh"
	"cw/camera.fxh"
	"jomini/jomini_colormap.fxh"
	"jomini/jomini_colormap_constants.fxh"
	"jomini/jomini_province_overlays.fxh"
	"sharedconstants.fxh"
	"constants_game.fxh"
	"coloroverlay_utility.fxh"
	"coloroverlay_powerbloc.fxh"
}

PixelShader = {

	TextureSampler FlagDiffuse
	{
		Index = 11
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		File = "gfx/map/textures/cloth.dds"
		srgb = yes
	}

	Code
	[[
		#define LAND_COLOR ToLinear( HSVtoRGB( float3( 0.11f, 0.06f, 0.89f ) ) )
		#define HIGHLIGHT_RANGE 0.5f

		// Stripes
		#define StripesGradientEdge 			0.25
		#define StripeMaskMin					0.5
		#define StripeMaskMax					1.5
		#define StripeMaskMultiplier			2.2

		#define StripeMaskEdgeMin				0.0
		#define StripeMaskEdgeMax				0.5
		#define StripeMaskEdgeMultiplier		2.2

		#define StripeOccupiedTransparency 		0.8
		#define StripeControlledColor 			float3( 1.000, 0.374, 0.100 )
		#define StripeControlledColorStrength 	2.5

		// Animated Stripe pulse
		#define StripePulseAngle 				-1.0
		#define StripePulseTiling 				150.0
		#define StripePulsePulseSpeed 			1.0

		// Coa Flags and Waving
		#define CoaControlledColor  			float3( 0.642, 0.321, 0.169 )
		#define CoaGradientEdge 				0.4
		#define CoaWaveScale 					100.0
		#define CoaWaveStrenght 				0.05
		#define CoaWaveSpeed 					0.5
		#define CoaWaveHighlight 				1.1
		#define CoaWaveShadow 					0.7
		#define CoaGapSize 						1.02
		#define CoaGapBlend 					0.02
		#define CoaClothSizeFlatmap				1.5

		void ApplyStripeColorBlend( float2 MapCoords, float2 ParallaxCoord, inout float3 Color, inout float PreLightingBlend, inout float PostLightingBlend )
		{
			// Coat of arms should only be shown in some map modes
			if( !_CoaConstants._Enabled )
			{
				return;
			}

			float2 SampledIds = SampleControllerIndex( MapCoords );
			float CountryId = SampledIds.r;
			float Occupied = SampledIds.g;
			float Controlled = 1.0 - Occupied;
			if( CountryId >= 0.0 )
			{
				float Opacity = 1.0f;
				#ifdef HIGH_QUALITY_SHADERS
					float2 Texel = vec2( 1.0f ) / _ProvinceMapSize;
					float2 Pixel = ( MapCoords * _ProvinceMapSize + 0.5 );
					float2 FracCoord = frac( Pixel );
					Pixel = floor( Pixel ) / _ProvinceMapSize - Texel * 0.5f;
					float C00 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel ).r ) );
					float C10 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + float2( Texel.x, 0.0 ) ).r ) );
					float C01 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + float2( 0.0, Texel.y ) ).r ) );
					float C11 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + Texel ).r ) );
					float x0 = lerp( C00, C10, FracCoord.x );
					float x1 = lerp( C01, C11, FracCoord.x );
					Opacity = RemapClamped( lerp( x0, x1, FracCoord.y ), 0.5f, 0.75f, 0.0f, 1.0f );
				#endif

				// Controller color
				float3 StripeColor = PdxTex2DLoad0( CountryColors, float2( CountryId, 0.0 ) ).rgb;

				// Opacity
				Opacity *= ( _CoaConstants._BlendStripes * ( 1.0f - _FlatmapLerp ) ) + ( _CoaConstants._BlendStripesFlatmap * _FlatmapLerp );
				Opacity = FadeCloseAlpha( Opacity );

				// Edge Gradient
				float4 ControllerColor = PdxTex2DLoad0( CountryColors, float2( CountryId, 0.0 ) );
				float Gradient = PdxTex2D( HighlightGradient, MapCoords ).g;
				Gradient = RemapClamped( Gradient, 0.0, StripesGradientEdge, 0.0, 1.0 );
				Gradient = saturate( Gradient );

				// Stripes
				float StripeScale = lerp( _CoaConstants._StripeScale, _CoaConstants._StripeScaleFlatmap, _FlatmapLerp );
				float StripeMask =  CalculateStripeMask( ParallaxCoord, 0.0, StripeScale );
				StripeMask = smoothstep( StripeMaskMin, StripeMaskMax, StripeMask * StripeMaskMultiplier );
				float StripeMaskEdge =  CalculateStripeMask( ParallaxCoord, 0.0, StripeScale );
				StripeMaskEdge = smoothstep( StripeMaskEdgeMin, StripeMaskEdgeMax, StripeMaskEdge * StripeMaskMultiplier );
				float StripeOpacity = StripeMaskEdge * Opacity;

				// Animated pulse
				float Pulse = ( sin( ( ( MapCoords.x + MapCoords.y * StripePulseAngle ) * StripePulseTiling ) - GlobalTime * StripePulsePulseSpeed ) * 0.4 + 0.6 );
				StripeColor = lerp( StripeColor, StripeColor * 2.0, Pulse * Controlled );
				Opacity = saturate( Opacity * StripeOpacity + Gradient * Controlled * Opacity );
				Opacity = lerp( Opacity, Opacity * StripeOccupiedTransparency, Occupied );

				// Controlled color
				float3 OccupiedColor = lerp( StripeColor * 0.75, StripeColor, StripeMask );
				float3 ControlledColor = StripeControlledColor * StripeControlledColorStrength;
				ControlledColor = lerp( StripeColor, ControlledColor * 1.5, Pulse );
				ControlledColor = lerp( ControlledColor, StripeColor, StripeMask );
				StripeColor = lerp( OccupiedColor, ControlledColor, Controlled );

				// Final Color
				Color = lerp( Color, StripeColor, StripeOpacity );
				Color = lerp( Color, ControllerColor, Gradient * Controlled );
				PreLightingBlend = lerp( PreLightingBlend, 0.0, Opacity );
				PostLightingBlend = lerp( PostLightingBlend, 1.0, Opacity );
			}
		}

		void ApplyCoaColorBlend( float2 MapCoords, float2 ParallaxCoord, inout float3 Color, inout float PreLightingBlend, inout float PostLightingBlend )
		{
			// Coat of arms should only be shown in some map modes
			if( !_CoaConstants._Enabled )
			{
				return;
			}

			// Provinces where Controller == Owner will have CountryId -1
			float2 SampledIds = SampleControllerIndex( MapCoords );
			float CountryId = SampledIds.r;
			float Occupied = SampledIds.g;
			float Controlled = 1.0 - Occupied;
			if( CountryId >= 0 )
			{
				// Wave Calculation
				float2 WaveUvOrigin = MapCoords;
				WaveUvOrigin.y -= 0.1;
				float WaveX = GlobalTime * CoaWaveSpeed - length( WaveUvOrigin * CoaWaveScale );
				float Wave = ( sin( 4.0 * sin( WaveX ) ) + 1.0 ) * 0.5;

				// Coa Calculation
				float Opacity = 1.0f;
				#ifdef HIGH_QUALITY_SHADERS
					float2 Texel = vec2( 1.0f ) / _ProvinceMapSize;
					float2 Pixel = ( MapCoords * _ProvinceMapSize + 0.5 );
					float2 FracCoord = frac( Pixel );
					Pixel = floor( Pixel ) / _ProvinceMapSize - Texel * 0.5f;
					float C00 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel ).r ) );
					float C10 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + float2( Texel.x, 0.0 ) ).r ) );
					float C01 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + float2( 0.0, Texel.y ) ).r ) );
					float C11 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + Texel ).r ) );
					float x0 = lerp( C00, C10, FracCoord.x );
					float x1 = lerp( C01, C11, FracCoord.x );
					Opacity = RemapClamped( lerp( x0, x1, FracCoord.y ), 0.5f, 0.75f, 0.0f, 1.0f );
				#endif

				float4 FlagUvs = PdxReadBuffer4( CountryCoaUvBuffer, CountryId );
				float2 CoaSize = _FlatmapLerp < 0.5f ? float2( _CoaConstants._Size, _CoaConstants._Size / _CoaConstants._AspectRatio ) : float2( _CoaConstants._SizeFlatmap, _CoaConstants._SizeFlatmap / _CoaConstants._AspectRatio );
				float2 CoaUv = ParallaxCoord * _ProvinceMapSize / CoaSize;
				CoaUv -= Wave * CoaWaveStrenght * Controlled;

				// Rotate
				float2 Rotation = float2( cos( _CoaConstants._Angle ), sin( _CoaConstants._Angle ) );
				CoaUv.x *= _CoaConstants._AspectRatio;
				CoaUv = float2( CoaUv.x * Rotation.x - CoaUv.y * Rotation.y, CoaUv.x * Rotation.y + CoaUv.y * Rotation.x );
				CoaUv.x /= _CoaConstants._AspectRatio;
				float2 CoaDdx = ddx( CoaUv );
				float2 CoaDdy = ddy( CoaUv );

				// Offset rows horizontally
				CoaUv.x += _CoaConstants._RowOffset * int( mod( CoaUv.y, _CoaConstants._RowCount ) );

				// Tile, flip, and scale to match the atlas
				CoaUv = frac( CoaUv );
				CoaUv.y = 1.0f - CoaUv.y;
				float GapX = CoaGapSize * mod( CoaUv.x, 1.0 ) ;
				float GapY = CoaGapSize * mod( CoaUv.y, 1.0 ) ;
				CoaUv = CoaGapSize * mod( CoaUv, 1.0 );
				CoaUv -= ( CoaGapSize - 1.0 ) * 0.5;
				CoaUv = FlagUvs.xy + CoaUv * FlagUvs.zw;

				// First blend in gradient border color on top of CoA color
				// Then adjust the border blend value so that CoA is always shown regardless of gradient
				float3 CoaColor = PdxTex2DGrad( CoaAtlas, CoaUv, CoaDdx, CoaDdy ).rgb;
				CoaColor = ToLinear( CoaColor );
				Opacity *= ( _CoaConstants._Blend * ( 1.0f - _FlatmapLerp ) ) + ( _CoaConstants._BlendFlatmap * _FlatmapLerp );
				Opacity = FadeCloseAlpha( Opacity );

				// Country inner edge color
				float OccupationOpacity = 0.90;
				float4 ControllerColor = PdxTex2DLoad0( CountryColors, float2( CountryId, 0.0 ) );
				Color = lerp( Color, ControllerColor, Controlled );
				Opacity = lerp( Opacity * OccupationOpacity, Opacity, Controlled );

				// Edge Gradient
				float Gradient = PdxTex2D( HighlightGradient, MapCoords ).g;
				Gradient = RemapClamped( Gradient, 0.0, CoaGradientEdge, 0.0, 1.0 );
				Gradient = saturate( Gradient );
				Opacity = lerp( Opacity, 0.0, Gradient );

				// Gap Color
				float3 GapColor = vec3( 0.025 );
				float3 ControlledGapColor = ToLinear( CoaControlledColor );
				float Gap = saturate( 1.0 - ( step( GapX, 1.0 ) * step( GapY, 1.0 ) ) );
				GapColor = lerp( GapColor, ControlledGapColor, Controlled );
				float GapXLerp = smoothstep( 1.0 - CoaGapBlend, 1.0, GapX - ( CoaGapSize - 1.0 ) * 0.5 );
				float GapYLerp = smoothstep( 1.0 - CoaGapBlend, 1.0, GapY - ( CoaGapSize - 1.0 ) * 0.5 );
				GapXLerp += smoothstep( CoaGapBlend, 0.0, GapX - ( CoaGapSize - 1.0 ) * 0.5 );
				GapYLerp += smoothstep( CoaGapBlend, 0.0, GapY - ( CoaGapSize - 1.0 ) * 0.5 );
				float GapLerp = saturate( GapXLerp + GapYLerp );
				CoaColor = lerp( CoaColor, ControllerColor.rgb * 0.5, GapLerp * Occupied );

				// Wave light and texture
				float2 TextureUv = ParallaxCoord * _ProvinceMapSize / CoaSize;
				TextureUv = lerp( TextureUv, TextureUv * CoaClothSizeFlatmap, _FlatmapLerp );
				TextureUv -= Wave * CoaWaveStrenght * Controlled;
				float3 ClothTexture = PdxTex2D( FlagDiffuse, TextureUv ).r * 4.0;
				CoaColor = Overlay( CoaColor, ClothTexture, 3.0 );

				Color = lerp( Color, CoaColor, Opacity );
				Color = lerp( Color, Overlay( GapColor, ClothTexture, 1.0 ) * 5.0 * ( Wave * 0.5 + 0.5 ), GapLerp * Controlled );
				Color = lerp( Color, Color * Wave * CoaWaveHighlight, CoaWaveShadow * Controlled * ( 1.0 - Gradient ) );

				// Country inner edge color
				PreLightingBlend = lerp( PreLightingBlend, 0.0, Opacity );
				PostLightingBlend = lerp( PostLightingBlend, 1.0, Opacity );
			}
 		}

		void ApplyMapTextureAndAlpha( inout float3 Color, inout float alpha, float Mask, float2 UV, int index )
		{
			float4 MapTexture = PdxTex2D( MapPaintingTextures, float3( UV, index ) );
			Color = lerp( Color, MapTexture.rgb, Mask * MapTexture.a );
			alpha = lerp( alpha, alpha * MapTexture.a, Mask );
		}

		void GameProvinceOverlayAndBlend( float2 ColorMapCoords, float3 WorldSpacePos, out float3 ColorOverlay, out float PreLightingBlend, out float PostLightingBlend )
		{
			// Paralx Coord
			float3 ToCam = normalize( CameraPosition - WorldSpacePos );
			float ParalaxDist = ( _ParallaxHeight - WorldSpacePos.y ) / ToCam.y;
			ParalaxDist = lerp ( ParalaxDist, 0.0, _FlatmapLerp );
			float3 ParallaxCoord = WorldSpacePos + ToCam * ParalaxDist;
			ParallaxCoord.xz = ParallaxCoord.xz * _WorldSpaceToTerrain0To1;

			// Gradient border values
			float DistanceFieldValue = CalcDistanceFieldValue( ColorMapCoords );
			float Edge = smoothstep( GB_EdgeWidth + max( 0.001f, GB_EdgeSmoothness ), GB_EdgeWidth, DistanceFieldValue );
			float GradientAlpha = lerp( GB_GradientAlphaInside, GB_GradientAlphaOutside, RemapClamped( DistanceFieldValue, GB_EdgeWidth + GB_GradientWidth, GB_EdgeWidth, 0.0f, 1.0f ) );

			// Default color
			ColorOverlay = LAND_COLOR;
			float4 ProvinceOverlayColorWithAlpha = vec4( 0.0f );

			// Color textures
			float4 PrimaryColor = BilinearColorSample( ColorMapCoords, IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture );
			float4 SecondaryColor = BilinearColorSampleAtOffset( ColorMapCoords, IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, SecondaryProvinceColorsOffset );
			float4 AlternateColor = BilinearColorSampleAtOffset( ColorMapCoords, IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, AlternateProvinceColorsOffset );

			// Primary as color or texture
			if ( !_UseMapmodeTextures )
			{
				// Get color
				ProvinceOverlayColorWithAlpha = AlphaBlendAOverB( PrimaryColor, SecondaryColor );
				ProvinceOverlayColorWithAlpha.rgb = lerp( ProvinceOverlayColorWithAlpha.rgb * GB_GradientColorMul, ProvinceOverlayColorWithAlpha.rgb * GB_EdgeColorMul, Edge );
				ProvinceOverlayColorWithAlpha.a = ProvinceOverlayColorWithAlpha.a * max( GradientAlpha, GB_EdgeAlpha * Edge );

				// Apply decentralized country color
				float4 DecentralizedColor = _DecentralizedCountryColor;
				float DecentralizedMask = saturate( 1.0f - Edge );

				DecentralizedColor.rgb = _DecentralizedCountryColor.rgb;
				DecentralizedColor.a *= AlternateColor.g;
				DecentralizedMask = DecentralizedMask * DecentralizedColor.a * _FlatmapLerp;
				ProvinceOverlayColorWithAlpha = lerp( ProvinceOverlayColorWithAlpha, DecentralizedColor, DecentralizedMask );

				// Apply impassable terrain color
				float4 ImpassableDiffuse = float4( PdxTex2D( ImpassableTerrainTexture, float2( ParallaxCoord.x * 2.0f, 1.0f - ParallaxCoord.z ) * _ImpassableTerrainTiling ).rgb,  AlternateColor.r );
				ImpassableDiffuse.rgb = Lighten( ImpassableDiffuse.rgb, _ImpassableTerrainColor.rgb );
				float ImpassableMask = ImpassableDiffuse.a * _ImpassableTerrainColor.a * ( 1.0f - _FlatmapLerp );

				// Fade impassable close
				ImpassableMask = FadeCloseAlpha( ImpassableMask );
				ProvinceOverlayColorWithAlpha = lerp( ProvinceOverlayColorWithAlpha, ImpassableDiffuse, ImpassableMask );

				// Get blendmode
				GetGradiantBorderBlendValues( ProvinceOverlayColorWithAlpha, PreLightingBlend, PostLightingBlend );

				// Apply impassable terrain blendmode
				PreLightingBlend = lerp( PreLightingBlend, 0.0f, ImpassableMask );
				PostLightingBlend = lerp( PostLightingBlend, 1.0f, ImpassableMask );

				// Apply output
				ColorOverlay = ProvinceOverlayColorWithAlpha.rgb;
			}
			else
			{
				float2 MapTextureUvSize = _FlatmapLerp < 0.5f ? _MapPaintingTextureTiling : _MapPaintingFlatmapTextureTiling;
				float2 MapTextureUv = float2( ParallaxCoord.x * 2.0f, 1.0f - ParallaxCoord.z ) * MapTextureUvSize;

				// Offset rows horizontally
				MapTextureUv.x += MAPMODE_UV_ROW_OFFSET * int( mod( MapTextureUv.y, MAPMODE_UV_ROW_COUNT ) );

				float MapTextureAlpha = 1.0f;
				float AlphaMask = 0.0f;

				if ( !_UsePrimaryRedAsGradient )
				{
					ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, PrimaryColor.r, MapTextureUv, 0 );
					AlphaMask += PrimaryColor.r;
				}
				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, PrimaryColor.g, MapTextureUv, 1 );
				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, PrimaryColor.b, MapTextureUv, 2 );
				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, PrimaryColor.a, MapTextureUv, 3 );

				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, SecondaryColor.r, MapTextureUv, 4 );
				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, SecondaryColor.g, MapTextureUv, 5 );
				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, SecondaryColor.b, MapTextureUv, 6 );
				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, SecondaryColor.a, MapTextureUv, 7 );

				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, AlternateColor.r, MapTextureUv, 8 );
				ApplyMapTextureAndAlpha( ColorOverlay, MapTextureAlpha, AlternateColor.g, MapTextureUv, 9 );

				AlphaMask += PrimaryColor.g + PrimaryColor.b + PrimaryColor.a;
				AlphaMask += SecondaryColor.r + SecondaryColor.g + SecondaryColor.b + SecondaryColor.a;
				AlphaMask += AlternateColor.r + AlternateColor.g;
				AlphaMask = saturate( AlphaMask * MapTextureAlpha );

				ProvinceOverlayColorWithAlpha.a = lerp( ProvinceOverlayColorWithAlpha.a, 1.0f, AlphaMask );

				ColorOverlay = lerp( ColorOverlay * GB_GradientColorMul, ColorOverlay * GB_EdgeColorMul, Edge );
				ProvinceOverlayColorWithAlpha.a = ProvinceOverlayColorWithAlpha.a * max( GradientAlpha * ( 1.0f - pow( Edge, 2 ) ), GB_EdgeAlpha * Edge );

				GetGradiantBorderBlendValues( ProvinceOverlayColorWithAlpha, PreLightingBlend, PostLightingBlend );
			}

			// Apply stylised noise
			// #ifndef LOW_QUALITY_SHADERS
			// 	#if defined( TERRAIN_FLAT_MAP ) || defined( TERRAIN_FLAT_MAP_LERP )
			// 		float DetailScale1 = 10.0f;
			// 		float DetailScale2 = 3.0f;
			// 		float DetailTexture1 = PdxTex2D( FlatmapNoiseMap, float2( ( ColorMapCoords.x * DetailScale1 * 2.0f ), 1.0f - ( ColorMapCoords.y * DetailScale1 ) ) ).g;
			// 		float DetailTexture2 = PdxTex2D( FlatmapNoiseMap, float2( ( ColorMapCoords.x * DetailScale2 * 2.0f ), 1.0f - ( ColorMapCoords.y * DetailScale2 ) ) ).g;
			// 		float DetailTexture3 = GetOverlay( DetailTexture1,  DetailTexture2, 1.0f );

			// 		// Don't blend in mapmodes
			// 		if ( !_UseMapmodeTextures )
			// 		{
			// 			ColorOverlay = saturate( GetOverlay( ColorOverlay, vec3( 1.0f - DetailTexture3 ), _FlatmapLerp ) );
			// 		}
			// 	#endif
			// #endif

			if( _CoaConstants._Enabled )
			{
				if ( _UseStripeOccupation == true )
				{
					ApplyStripeColorBlend( ColorMapCoords, ParallaxCoord.xz, ColorOverlay, PreLightingBlend, PostLightingBlend );
				}
				else
				{
					ApplyCoaColorBlend( ColorMapCoords, ParallaxCoord.xz, ColorOverlay, PreLightingBlend, PostLightingBlend );
				}
			}

			if ( _EnableMapPowerBloc == true )
			{
				ApplyPowerBlocOverlay( ColorOverlay, ProvinceOverlayColorWithAlpha.a, ColorMapCoords, WorldSpacePos.xz );
			}

			PreLightingBlend *= _OverlayOpacity;
			PostLightingBlend *= _OverlayOpacity;
		}

		float3 ApplyDynamicFlatmap( float3 FlatmapDiffuse, float2 ColorMapCoords, float2 WorldSpacePosXZ )
		{
			float ExtentStr = _ShorelineExtentStr;
			float Alpha = _ShorelineAlpha;
			float UVScale = _ShoreLinesUVScale;

			#ifndef LOW_QUALITY_SHADERS
				float MaskBlur = _ShorelineMaskBlur;
				float LandMaskBlur = PdxTex2DLod( LandMaskMap, float2( ColorMapCoords.x, 1.0f - ColorMapCoords.y ), MaskBlur ).r;
				float ShoreLines = PdxTex2D( FlatmapNoiseMap, ColorMapCoords * UVScale ).r;
				ShoreLines *= saturate( Alpha );
			#endif

			float LandMask = 0.0f;
			float ShoreLinesStripes = 0.0f;

			float4 AlternateColor = BilinearColorSampleAtOffset( ColorMapCoords, IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, AlternateProvinceColorsOffset );
			AlternateColor.rg = vec2( 0.0f ); // Zero out unused channels to avoid issues
			float4 LakeColor = float4( 0.0f, 0.0f, 0.0f, 1.0f ); // Needs to match color in mappaintingmanager.cpp
			float4 SeaColor = float4( 0.0f, 0.0f, 1.0f, 0.0f );	// Needs to match color in mappaintingmanager.cpp
			float4 LakeDiff = LakeColor - AlternateColor;
			float4 SeaDiff = SeaColor - AlternateColor;
			float4 LakeSeaDiff = dot( LakeDiff, LakeDiff ) * dot( SeaDiff, SeaDiff );

			// Land color
			float3 Land = LAND_COLOR;
			float OutlineValue = 1.0f - smoothstep( 0.75f, 1.0f, LakeSeaDiff );
			Land = lerp( Land, FlatmapDiffuse, OutlineValue );

			// Not a lake and doesn't have water mass
			if( dot( LakeDiff, LakeDiff ) > 0.1f )
			{
				#ifndef LOW_QUALITY_SHADERS
					ShoreLinesStripes = saturate( LandMaskBlur * ShoreLines * _ShorelineExtentStr );
				#endif
				ShoreLinesStripes = saturate( ShoreLinesStripes * _ShorelineAlpha );
				ShoreLinesStripes = clamp( ShoreLinesStripes, 0.0, 0.5f );
				FlatmapDiffuse = lerp( FlatmapDiffuse, vec3( 0.0f ), ShoreLinesStripes );

				// Not sea, so apply land mask
				if( dot( SeaDiff, SeaDiff ) > 0.1f )
				{
					LandMask = LakeSeaDiff;
				}
			}

			// Blends in shorelines/flatmap color adjustments
			FlatmapDiffuse = lerp( FlatmapDiffuse, Land, LandMask );

			return FlatmapDiffuse;
		}

		// Convenicence function for changing blend modes in all shaders
		float3 ApplyColorOverlay( float3 Color, float3 ColorOverlay, float Blend )
		{
			float3 HSV_ = RGBtoHSV( ColorOverlay.rgb );
			HSV_.x += 0.0f;		// Hue
			HSV_.y *= 0.95f; 	// Saturation
			HSV_.z *= 0.35f;	// Value
			ColorOverlay.rgb = lerp( ColorOverlay.rgb, HSVtoRGB( HSV_ ), 1.0f - _FlatmapLerp );

			Color = lerp( Color, ColorOverlay, Blend );
			return Color;
		}

		float3 ApplyHighlight( float3 Color, float2 Coordinate )
		{
			float Gradient = PdxTex2D( HighlightGradient, Coordinate ).r;

			float SingleSamplingSafeDistance = 0.49f;
			float4 HighlightColor = vec4( 0 );
			if( abs( 0.5f - PdxTex2D( HighlightGradient, Coordinate ).r ) > SingleSamplingSafeDistance )
			{
				// Optimisation - We can use the gradient to quickly gauge where it's safe to use a single sample
				// If the gradient is close to 0.5 then there is a color change somewhere nearby, and multi sampling is needed.
				// Otherwise a single sample will do
				HighlightColor = ColorSampleAtOffset( Coordinate, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
			}
			else
			{
			#ifdef HIGH_QUALITY_SHADERS
				// Lots of double samples here
				// There's no meassurable difference between this naive implementation and a bespoke
				// implementation for reducing the number of samples (on GTX 1080Ti) so assuming the
				// the texture cache is able to handle this just fine.
				// Naive implementation reduces code duplication and makes code simpler
				float2 Offset = InvIndirectionMapSize;
				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2( -1, -1 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2(  0, -1 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2(  1, -1 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );

				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2( -1,  0 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2(  0,  0 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2(  1,  0 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );

				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2( -1,  1 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2(  0,  1 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
				HighlightColor += BilinearColorSampleAtOffset( Coordinate + Offset * float2(  1,  1 ), IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
				HighlightColor /= 9.0f;
			#else
				HighlightColor = BilinearColorSampleAtOffset( Coordinate, IndirectionMapSize, InvIndirectionMapSize, ProvinceColorIndirectionTexture, ProvinceColorTexture, HighlightProvinceColorsOffset );
			#endif
			}

			HighlightColor.a *= 1.0f - Gradient;
			HighlightColor.a = RemapClamped( HighlightColor.a, 0.0f, HIGHLIGHT_RANGE, 0.0f, 1.0f );

			Color = lerp( Color, HighlightColor.rgb, HighlightColor.a );
			return Color;
		}
	]]
}
