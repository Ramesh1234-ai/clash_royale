from flask import Blueprint, jsonify, request
from services.roast_service import generate_roast
from services.player_service import PlayerService
from services.clash_royale import ClashRoyaleAPIError

roast_bp = Blueprint('roast', __name__, url_prefix='/api/roast')


@roast_bp.route('/<player_tag>', methods=['GET'])
def roast_player(player_tag):

    intensity = request.args.get('intensity', 'fun')
    if intensity not in ['fun', 'savage', 'nuclear']:
        intensity = 'fun'

    # Normalize tag
    player_tag = player_tag.upper()
    if not player_tag.startswith('#'):
        player_tag = f'#{player_tag}'

    try:
        player_data = PlayerService.get_or_create_player(player_tag)

        if not player_data:
            return jsonify({
                'success': False,
                'error': 'Player not found'
            }), 404

        roast = generate_roast(player_data, intensity=intensity)

        return jsonify({
            'success': True,
            'data': {
                'player': player_data.get('name', player_tag),
                'roast': roast,
                'intensity': intensity
            }
        }), 200

    except ClashRoyaleAPIError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to generate roast'
        }), 500