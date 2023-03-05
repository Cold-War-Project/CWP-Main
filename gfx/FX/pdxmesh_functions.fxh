Includes = {
	"cw/pdxmesh.fxh"
	"cw/camera.fxh"
	"jomini/jomini_water.fxh"
	"sharedconstants.fxh"
}

VertexShader =
{
	TextureSampler WindMapTree
	{
		Ref = WindMapTree
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
	TextureSampler FlowMapTexture
	{
		Ref = JominiWaterTexture2
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}
}

VertexShader =
{
	Code
	[[

		void CalculateSineAnimation( float2 UV, inout float3 Position, inout float3 Normal, inout float4 Tangent )
		{
			float AnimSeed = UV.x;
			const float LARGE_WAVE_FREQUENCY = 3.14f;	// Higher values simulates higher wind speeds / more turbulence
			const float SMALL_WAVE_FREQUENCY = 9.0f;	// Higher values simulates higher wind speeds / more turbulence
			const float WAVE_LENGTH_POW = 2.0f;			// Higher values gives higher frequency at the end of the flag
			const float WAVE_LENGTH_INV_SCALE = 7.0f;	// Higher values gives higher frequency overall
			const float WAVE_SCALE = 0.1f;				// Higher values gives a stretchier flag
			const float ANIMATION_SPEED = 0.5f;			// Speed

			float Time = GlobalTime * 1.0f * ANIMATION_SPEED;

			float LargeWave = sin( Time * LARGE_WAVE_FREQUENCY );
			float SmallWaveV = Time * SMALL_WAVE_FREQUENCY - pow( AnimSeed, WAVE_LENGTH_POW ) * WAVE_LENGTH_INV_SCALE;
			float SmallWaveD = -( WAVE_LENGTH_POW * pow( AnimSeed, WAVE_LENGTH_POW ) * WAVE_LENGTH_INV_SCALE );
			float SmallWave = sin( SmallWaveV );
			float CombinedWave = SmallWave + LargeWave;

			float Wave = WAVE_SCALE * AnimSeed * CombinedWave;
			float Derivative = WAVE_SCALE * ( LargeWave + SmallWave + cos( SmallWaveV ) * SmallWaveD );
			float3 AnimationDir = float3( 0, 0.08, -1 );	// cross( Tangent.xyz, float3(0,1,0) );
			Position += AnimationDir * Wave;

			float2 WaveTangent = normalize( float2( 1.0f, Derivative ) );
			float3 WaveNormal = normalize( float3( WaveTangent.y, 0.0f, -WaveTangent.x ));
			float WaveNormalStrength = 1.0f;
			Normal = normalize( lerp( Normal, WaveNormal, 1.0f * AnimSeed ) ); // wave normal strength
		}

		float3 WindTransform( float3 Position, float4x4 WorldMatrix )
		{
			float3 WorldSpacePos = mul( WorldMatrix, float4( Position, 1.0f ) ).xyz;
			float2 MapCoords = float2( WorldSpacePos.x / MapSize.x, 1.0 - WorldSpacePos.z / MapSize.y );

			float3 FlowMap = PdxTex2DLod0( FlowMapTexture, MapCoords ).rgb;
			float3 FlowDir = FlowMap.xyz * 2.0 - 1.0;
			FlowDir = FlowDir / ( length( FlowDir ) + 0.000001 ); // Intel did not like normalize()

			float WindMap = PdxTex2DLod0( WindMapTree, MapCoords ).r;

			float WorldX = GetMatrixData( WorldMatrix, 0, 3 );
			float WorldY = GetMatrixData( WorldMatrix, 2, 3 );
			float Noise = CalcNoise( GlobalTime * TreeSwayLoopSpeed + TreeSwayWindStrengthSpatialModifier * float2( WorldX, WorldY ) );
			float WindSpeed = Noise * Noise;
			float Phase = GlobalTime * TreeSwaySpeed + TreeSwayWindClusterSizeModifier * ( WorldX + WorldY );
			float3 Offset = normalize( float3( FlowDir.x, 0.0f, FlowDir.z ) );
			Offset = mul( Offset, CastTo3x3( WorldMatrix ) );
			float HeightFactor = saturate( Position.y * TreeHeightImpactOnSway );
			HeightFactor *= HeightFactor;

			float wave = sin( Phase ) + 0.5f;
			Position += TreeSwayScale * WindMap * HeightFactor * wave * Offset * WindSpeed;

			return Position;
		}

		float3 WindTransformBush( float3 Position, float4x4 WorldMatrix )
		{
			float3 WorldSpacePos = mul( WorldMatrix, float4( Position, 1.0f ) ).xyz;
			float2 MapCoords = float2( WorldSpacePos.x / MapSize.x, 1.0 - WorldSpacePos.z / MapSize.y );

			float3 FlowMap = PdxTex2DLod0( FlowMapTexture, MapCoords ).rgb;
			float3 FlowDir = FlowMap.xyz * 2.0 - 1.0;
			FlowDir = FlowDir / ( length( FlowDir ) + 0.000001 ); // Intel did not like normalize()

			float WindMap = PdxTex2DLod0( WindMapTree, MapCoords ).r;

			float WorldX = GetMatrixData( WorldMatrix, 0, 3 );
			float WorldY = GetMatrixData( WorldMatrix, 2, 3 );
			float Noise = CalcNoise( GlobalTime * TreeSwayLoopSpeed + TreeSwayWindStrengthSpatialModifier * float2( WorldX, WorldY ) );
			float WindSpeed = Noise * Noise;
			float Phase = GlobalTime * TreeSwaySpeed + TreeSwayWindClusterSizeModifier * ( WorldX + WorldY );
			float3 Offset = normalize( float3( FlowDir.x, 0.0f, FlowDir.z ) );
			Offset = mul( Offset, CastTo3x3( WorldMatrix ) );
			float HeightFactor = saturate( Position.y * TreeHeightImpactOnSway * BUSH_TREE_HEIGHT_IMPACT );
			HeightFactor *= HeightFactor;

			float wave = sin( Phase ) + 0.5f;
			Position += TreeSwayScale * BUSH_TREE_SWAY_SCALE * WindMap * HeightFactor * wave * Offset * WindSpeed;

			return Position;
		}

		float3 WindTransformMedium( float3 Position, float4x4 WorldMatrix )
		{
			float3 WorldSpacePos = mul( WorldMatrix, float4( Position, 1.0f ) ).xyz;
			float2 MapCoords = float2( WorldSpacePos.x / MapSize.x, 1.0 - WorldSpacePos.z / MapSize.y );

			float3 FlowMap = PdxTex2DLod0( FlowMapTexture, MapCoords ).rgb;
			float3 FlowDir = FlowMap.xyz * 2.0 - 1.0;
			FlowDir = FlowDir / ( length( FlowDir ) + 0.000001 ); // Intel did not like normalize()

			float WindMap = PdxTex2DLod0( WindMapTree, MapCoords ).r;

			float WorldX = GetMatrixData( WorldMatrix, 0, 3 );
			float WorldY = GetMatrixData( WorldMatrix, 2, 3 );
			float Noise = CalcNoise( GlobalTime * TreeSwayLoopSpeed + TreeSwayWindStrengthSpatialModifier * float2( WorldX, WorldY ) );
			float WindSpeed = Noise * Noise;
			float Phase = GlobalTime * TreeSwaySpeed * MEDIUM_TREE_SWAY_SPEED + TreeSwayWindClusterSizeModifier * ( WorldX + WorldY );
			float3 Offset = normalize( float3( FlowDir.x, 0.0f, FlowDir.z ) );
			Offset = mul( Offset, CastTo3x3( WorldMatrix ) );
			float HeightFactor = saturate( Position.y * TreeHeightImpactOnSway * MEDIUM_TREE_HEIGHT_IMPACT );
			HeightFactor *= HeightFactor;

			float wave = sin( Phase ) + 0.5f;
			Position += TreeSwayScale * MEDIUM_TREE_SWAY_SCALE * WindMap * HeightFactor * wave * Offset * WindSpeed;

			return Position;
		}

		float3 WindTransformTall( float3 Position, float4x4 WorldMatrix )
		{
			float3 WorldSpacePos = mul( WorldMatrix, float4( Position, 1.0f ) ).xyz;
			float2 MapCoords = float2( WorldSpacePos.x / MapSize.x, 1.0 - WorldSpacePos.z / MapSize.y );

			float3 FlowMap = PdxTex2DLod0( FlowMapTexture, MapCoords ).rgb;
			float3 FlowDir = FlowMap.xyz * 2.0 - 1.0;
			FlowDir = FlowDir / ( length( FlowDir ) + 0.000001 ); // Intel did not like normalize()

			float WindMap = PdxTex2DLod0( WindMapTree, MapCoords ).r;

			float WorldX = GetMatrixData( WorldMatrix, 0, 3 );
			float WorldY = GetMatrixData( WorldMatrix, 2, 3 );
			float Noise = CalcNoise( GlobalTime * TreeSwayLoopSpeed + TreeSwayWindStrengthSpatialModifier * float2( WorldX, WorldY ) );
			float WindSpeed = Noise * Noise;
			float Phase = GlobalTime * TreeSwaySpeed * TALL_TREE_SWAY_SPEED + TreeSwayWindClusterSizeModifier * ( WorldX + WorldY );
			float3 Offset = normalize( float3( FlowDir.x, 0.0f, FlowDir.z ) );
			Offset = mul( Offset, CastTo3x3( WorldMatrix ) );
			float HeightFactor = saturate( Position.y * TreeHeightImpactOnSway * TALL_TREE_HEIGHT_IMPACT );
			HeightFactor *= HeightFactor;

			float wave = sin( Phase ) + 0.5f;
			Position += TreeSwayScale * TALL_TREE_SWAY_SCALE * WindMap * HeightFactor * wave * Offset * WindSpeed;

			return Position;
		}

		float3 SnapToWaterLevel( float3 PositionY, float4x4 WorldMatrix )
		{
			float3 WorldSpacePos = mul( WorldMatrix, float4( float3( 0.0f, 0.0f, 0.0f ), 1.0f ) ).xyz;

			float Height = GetHeight( WorldSpacePos.xz );
			PositionY += ( _WaterHeight - WorldSpacePos.y );

			return PositionY;
		}

	]]

}