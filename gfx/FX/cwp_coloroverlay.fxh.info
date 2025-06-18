Includes = {
	"cw/terrain.fxh"
	"jomini/jomini_colormap.fxh"
	"jomini/jomini_colormap_constants.fxh"
	"jomini/jomini_province_overlays.fxh"
	"cw/utility.fxh"
	"cw/camera.fxh"
	"sharedconstants.fxh"
	"constants_game.fxh"
}

PixelShader = {

	TextureSampler FlatmapNoiseMap
	{
		Index = 7
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		File = "gfx/map/textures/flatmap_noise.dds"
		srgb = no
	}

	TextureSampler LandMaskMap
	{
		Index = 9
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		File = "gfx/map/textures/land_mask.dds"
		srgb = yes
	}

	#// Highlight in Red
	#// Occupatioon in Green
	TextureSampler HighlightGradient
	{
		Ref = HighlightGradient
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}

	TextureSampler ImpassableTerrainTexture
	{
		Ref = ImpassableTerrain
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}

	TextureSampler MapPaintingTextures
	{
		Ref = MapPaintingTexturesRef
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		type = "2darray"
	}
	TextureSampler FlatmapOverlayTexture
	{
		Ref = FlatmapOverlay
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Clamp"
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

	TextureSampler CoaAtlas
	{
		Ref = CoaAtlasTexture
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	BufferTexture ProvinceCountryIdBuffer
	{
		Ref = ProvinceCountryId
		type = int
	}
	BufferTexture ProvinceControllerIdBuffer
	{
		Ref = ProvinceControllerId
		type = int
	}
	BufferTexture CountryCoaUvBuffer
	{
		Ref = CountryFlagUvs
		type = float4
	}

	Code
	[[
		#define LAND_COLOR ToLinear( HSVtoRGB( float3( 0.11f, 0.06f, 0.89f ) ) )
		#define HIGHLIGHT_RANGE 0.5f

		int SampleCountryIndex( float2 MapCoords )
		{
			float2 ColorIndex = PdxTex2D( ProvinceColorIndirectionTexture, MapCoords ).rg;
			int Index = ColorIndex.x * 255.0 + ColorIndex.y * 255.0 * 256.0;
			return PdxReadBuffer( ProvinceCountryIdBuffer, Index ).r;
		}
		int SampleControllerIndex( float2 MapCoords )
		{
			float2 ColorIndex = PdxTex2D( ProvinceColorIndirectionTexture, MapCoords ).rg;
			int Index = ColorIndex.x * 255.0 + ColorIndex.y * 255.0 * 256.0;
			return PdxReadBuffer( ProvinceControllerIdBuffer, Index ).r;
		}

		void ApplyStripeColorBlend( float2 MapCoords, float2 ParalaxCoord, inout float3 Color, inout float PreLightingBlend )
		{
			// Coat of arms should only be shown in some map modes
			if( !_CoaConstants._MapCoaEnabled )
			{
				return;
			}

			int CountryId = SampleControllerIndex( MapCoords );
			if( CountryId >= 0 )
			{
				float Opacity = 1.0f;
				#ifdef HIGH_QUALITY_SHADERS
					float2 Texel = vec2( 1.0f ) / _ProvinceMapSize;
					float2 Pixel = ( MapCoords * _ProvinceMapSize + 0.5 );
					float2 FracCoord = frac( Pixel );
					Pixel = floor( Pixel ) / _ProvinceMapSize - Texel * 0.5f;
					float C00 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel ) ) );
					float C10 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + float2( Texel.x, 0.0 ) ) ) );
					float C01 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + float2( 0.0, Texel.y ) ) ) );
					float C11 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + Texel ) ) );
					float x0 = lerp( C00, C10, FracCoord.x );
					float x1 = lerp( C01, C11, FracCoord.x );
					Opacity = RemapClamped( lerp( x0, x1, FracCoord.y ), 0.5f, 0.75f, 0.0f, 1.0f );
				#endif

				float4 StripeColor = PdxTex2DLoad0( CountryColors, int2( CountryId, 0 ) );

				Opacity *= ( _CoaConstants._MapCoaBlendOccupation * ( 1.0f - _FlatmapLerp ) ) + ( _CoaConstants._MapCoaBlendOccupationFlatmap * _FlatmapLerp );

				float FadeStart = ( _CoaConstants._MapCoaBlendFadeStart - _CoaConstants._MapCoaBlendFadeEnd );
				float CloseZoomBlend = FadeStart - CameraPosition.y + ( _CoaConstants._MapCoaBlendFadeEnd );
				CloseZoomBlend = smoothstep( FadeStart, 0.0f, CloseZoomBlend );
				Opacity *= CloseZoomBlend;

				float StripeScale = lerp( _CoaConstants._MapCoaStripeScale, _CoaConstants._MapCoaStripeScaleFlatmap, _FlatmapLerp );
				Opacity *= CalculateStripeMask( MapCoords, 0.0, StripeScale );

				float Gradient = 1.0 - PdxTex2D( HighlightGradient, MapCoords ).g;
				float GradientAdd = LevelsScan( Gradient, OCCUPATION_HIGHLIGHT_POSITION, OCCUPATION_HIGHLIGHT_CONTRAST );
				float HighlightAlpha = GradientAdd * Gradient;
				float3 HighlightColor = StripeColor.rgb * OCCUPATION_HIGHLIGHT_COLOR_MULT;

				PreLightingBlend = saturate( Opacity + PreLightingBlend + HighlightAlpha);

				Color = lerp( Color, StripeColor.rgb, Opacity );
				Color = lerp( Color, saturate( HighlightColor ), saturate( HighlightAlpha * OCCUPATION_HIGHLIGHT_STRENGTH ) * OCCUPATION_HIGHLIGHT_ALPHA );
			}
		}

		void ApplyCoaColorBlend( float2 MapCoords, float2 ParalaxCoord, inout float3 Color, inout float PreLightingBlend )
		{
			// Coat of arms should only be shown in some map modes
			if( !_CoaConstants._MapCoaEnabled )
			{
				return;
			}

			// Provinces where Controller == Owner will have CountryId -1
			int CountryId = SampleControllerIndex( MapCoords );
			if( CountryId >= 0 )
			{
				float Opacity = 1.0f;
				#ifdef HIGH_QUALITY_SHADERS
					float2 Texel = vec2( 1.0f ) / _ProvinceMapSize;
					float2 Pixel = ( MapCoords * _ProvinceMapSize + 0.5 );
					float2 FracCoord = frac( Pixel );
					Pixel = floor( Pixel ) / _ProvinceMapSize - Texel * 0.5f;
					float C00 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel ) ) );
					float C10 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + float2( Texel.x, 0.0 ) ) ) );
					float C01 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + float2( 0.0, Texel.y ) ) ) );
					float C11 = 1.0f - saturate( abs( CountryId - SampleControllerIndex( Pixel + Texel ) ) );
					float x0 = lerp( C00, C10, FracCoord.x );
					float x1 = lerp( C01, C11, FracCoord.x );
					Opacity = RemapClamped( lerp( x0, x1, FracCoord.y ), 0.5f, 0.75f, 0.0f, 1.0f );
				#endif
				float4 FlagUvs = PdxReadBuffer4( CountryCoaUvBuffer, CountryId );
				float2 CoaSize = _FlatmapLerp < 0.5f ? float2( _CoaConstants._MapCoaSize, _CoaConstants._MapCoaSize / _CoaConstants._MapCoaAspectRatio ) : float2( _CoaConstants._MapCoaSizeFlatmap, _CoaConstants._MapCoaSizeFlatmap / _CoaConstants._MapCoaAspectRatio );
				float2 CoaUV = ParalaxCoord * _ProvinceMapSize / CoaSize;

				// Rotate
				float2 Rotation = float2( cos( _CoaConstants._MapCoaAngle ), sin( _CoaConstants._MapCoaAngle ) );
				CoaUV.x *= _CoaConstants._MapCoaAspectRatio;
				CoaUV = float2( CoaUV.x * Rotation.x - CoaUV.y * Rotation.y, CoaUV.x * Rotation.y + CoaUV.y * Rotation.x );
				CoaUV.x /= _CoaConstants._MapCoaAspectRatio;

				float2 CoaDdx = ddx( CoaUV );
				float2 CoaDdy = ddy( CoaUV );

				// Offset rows horizontally
				CoaUV.x += _CoaConstants._MapCoaRowOffset * int( mod( CoaUV.y, _CoaConstants._MapCoaRowCount ) );

				// Tile, flip, and scale to match the atlas
				CoaUV = frac( CoaUV );
				CoaUV.y = 1.0f - CoaUV.y;
				CoaUV = FlagUvs.xy + CoaUV * FlagUvs.zw;

				// First blend in gradient border color on top of CoA color
				// Then adjust the border blend value so that CoA is always shown regardless of gradient
				float3 CoaColor = PdxTex2DGrad( CoaAtlas, CoaUV, CoaDdx, CoaDdy ).rgb;
				CoaColor = ToLinear( CoaColor );

				Opacity *= ( _CoaConstants._MapCoaBlend * ( 1.0f - _FlatmapLerp ) ) + ( _CoaConstants._MapCoaBlendFlatmap * _FlatmapLerp );

				float FadeStart = ( _CoaConstants._MapCoaBlendFadeStart - _CoaConstants._MapCoaBlendFadeEnd );
				float CloseZoomBlend = FadeStart - CameraPosition.y + ( _CoaConstants._MapCoaBlendFadeEnd );
				CloseZoomBlend = smoothstep( FadeStart, 0.0f, CloseZoomBlend );
				Opacity *= CloseZoomBlend;

				PreLightingBlend = max( Opacity, PreLightingBlend );

				// Occupation highlight
				float Gradient = 1.0 - PdxTex2D( HighlightGradient, MapCoords ).g;
				float GradientAdd = LevelsScan( Gradient, OCCUPATION_HIGHLIGHT_POSITION, OCCUPATION_HIGHLIGHT_CONTRAST );
				float HighlightAlpha = Opacity * GradientAdd * Gradient;
				float3 HighlightColor = Color * OCCUPATION_HIGHLIGHT_COLOR_MULT;

				Color = lerp( Color, saturate( CoaColor ), Opacity );
				Color = lerp( Color, saturate( HighlightColor ), saturate( HighlightAlpha * OCCUPATION_HIGHLIGHT_STRENGTH ) * OCCUPATION_HIGHLIGHT_ALPHA );
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
			float ParalaxDist = ( _ImpassableTerrainHeight - WorldSpacePos.y ) / ToCam.y;
			float3 ParalaxCoord = WorldSpacePos + ToCam * ParalaxDist;
			ParalaxCoord.xz = ParalaxCoord.xz * _WorldSpaceToTerrain0To1;

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

			// Land/Ocean/Lake masks
			float LandMask = PdxTex2DLod0( LandMaskMap, float2( ColorMapCoords.x, 1.0f - ColorMapCoords.y ) ).r;
			float EndLandMask = 0.0f;
			float ShoreLinesStripes = 0.0f;

			// Primary as texture or color
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
				float4 ImpassableDiffuse = float4( PdxTex2D( ImpassableTerrainTexture, float2( ParalaxCoord.x * 2.0f, 1.0f - ParalaxCoord.z ) * _ImpassableTerrainTiling ).rgb,  AlternateColor.r );
				ImpassableDiffuse.rgb = Lighten( ImpassableDiffuse.rgb, _ImpassableTerrainColor.rgb );
				float ImpassableMask = ImpassableDiffuse.a * _ImpassableTerrainColor.a * ( 1.0f - _FlatmapLerp );

				// Fade impassable close
				float FadeStart = ( _DistanceFadeStart - _DistanceFadeEnd );
				float CloseZoomBlend = FadeStart - CameraPosition.y + _DistanceFadeEnd;
				CloseZoomBlend = smoothstep( FadeStart, 0.0f, CloseZoomBlend );
				ImpassableMask *= CloseZoomBlend;
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
				float2 MapTextureUv = float2( ParalaxCoord.x * 2.0f, 1.0f - ParalaxCoord.z ) * MapTextureUvSize;

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

			if ( _UseStripeOccupation == true )
			{
				ApplyStripeColorBlend( ColorMapCoords, ParalaxCoord.xz, ColorOverlay, PreLightingBlend );
			}
			else
			{
				ApplyCoaColorBlend( ColorMapCoords, ParalaxCoord.xz, ColorOverlay, PreLightingBlend );
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
