# #Delta's Chess

# import pyglet
# # from pieces import *
# from game import *


# def render_game(game:"Board", player):

#     render_board(game)
#     render_moves(game, player)    
#     render_pieces(game, player)


# def render_board(board:"Board"):
#     color = ((0,0,0,0), (245, 245, 245, 255), (10, 10, 10, 255))
#     e = 1
#     i = 1
#     for x in range(len(board)):
#         for y in range(len(board[0])):
#             pyglet.shapes.Rectangle(x=x*64, y=y*64, width=64, height=64, color=color[i]).draw()
#             i = -i
#         e = -e
#         i = e
#     pyglet.shapes.Rectangle(x=8*64 + 8, y=0, width=16, height=64*8, color=color[1 if board.turn%2 == 0 else -1]).draw()

# def render_pieces(board:"Board", player):
#     side = 0
#     if player == 1:
#         side = 7
#     for t in board.team_list:
#         for p in t:
#             a = pyglet.sprite.Sprite(img=pyglet.image.load(f'code/python/wip-delta_s_chess/textures/{p.name}{"_b" if p.color == 1 else ""}.png'),
#                                      x=abs(side - p.pos.x)*64, y=abs(side - p.pos.y)*64)
#             a.scale = 4
#             a.draw()

# def render_moves(board:"Board", player):
#     if board.selected_piece:
#         side = 0
#         if player == 1:
#             side = 7
#         for m in board.selected_piece.moves:
#             pyglet.shapes.Rectangle(x=abs(side - m.x)*64 + 8, y=abs(side - m.y)*64 + 8, width=48, height=48, color=(100, 255, 100, 255)).draw()
#         for m in board.selected_piece.controlled_squares:
#             pyglet.shapes.Rectangle(x=abs(side - m.x)*64 + 16, y=abs(side - m.y)*64 + 16, width=32, height=32, color=(255, 100, 100, 255)).draw()
