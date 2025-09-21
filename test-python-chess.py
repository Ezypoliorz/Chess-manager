import chess
import chess.svg
import base64

# Créez une nouvelle partie
board = chess.Board()

# Lire le fichier SVG des pièces
# Supposons que vous avez un fichier SVG pour le pion blanc
# Vous devrez le faire pour toutes les pièces (roi, dame, etc.)
try:
    with open("bp.svg", "rb") as f:
        pawn_svg_data = base64.b64encode(f.read()).decode("utf-8")
except FileNotFoundError:
    pawn_svg_data = "" # Si le fichier n'est pas trouvé

# Définissez une feuille de style CSS pour le plateau
custom_style = f"""
    #black-pawn {{
        background-image: url("data:image/svg+xml;base64,{pawn_svg_data}");
        background-repeat: no-repeat;
        background-size: 100% 100%;
    }}
    .piece {{
        fill: none;
    }}
"""

# Créer le plateau
svg_data = chess.svg.board(
    board=board,
    style=custom_style,
    size=400
)

# Sauvegarder l'image
with open("board_with_custom_pieces.svg", "w") as f:
    f.write(svg_data)