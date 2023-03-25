from settings import coeff
#data = [(offset_x,offset_y),(hitbox_w,hitbox_h), flip_offset, attack_width]

santa_dico_v1 = {
    'Santa/Santa_SpriteSheet.png' : [[22], [5,8,4,4,6,8,6,6,5,4,7,1,1,1,1,1,1,1,1,1,1,9]]}
santa_data = ([3,35],[19,29], 71, 17)
santa_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2,2,3,3,5,6],
    'Hit' : [9],
    'Death' : [10]}
santa_stats = {
    'health': 110,
    'speed': coeff*2/3,
    'attack': 13,
    'attack_speed': 16,
    'stamina': 130}


minotaur_dico_v1 = {
    'Minotaur/Minotaur_Spritesheet.png' : [[10],[5,8,5,9,5,6,6,3,3,6]]}
minotaur_data = ([32,24],[30,34],1, 27)
minotaur_indexs = {
    'Idle' : [0,0,0,2],
    'Walk' : [1],
    'Attack' : [3,4,6],
    'Hit' : [8],
    'Death' : [9]}
minotaur_stats = {
    'health': 190,
    'speed': coeff,
    'attack': 24,
    'attack_speed': 14,
    'stamina': 130}

dwarf_dico_v1 = {
    'Dwarf/Dwarf_SpriteSheet.png' : [[8],[5,8,7,6,2,5,4,7]]}
dwarf_data = ([26,10],[11,19],1,14)
dwarf_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2,3,4],
    'Hit' : [6],
    'Death' : [7]}
dwarf_stats = {
    'health': 93,
    'speed': coeff*4/3,
    'attack': 9,
    'attack_speed': 24,
    'stamina': 120}


indiana_jones_dico_v1 = {
    'Indiana_Jones/Indiana_Jones_SpriteSheet.png' : [[7],[8,8,7,6,8,4,5]]}
indiana_jones_data = ([26,10],[11,22],1, 25)
indiana_jones_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [4,4,5],
    'Hit' : [2],
    'Death' : [6]}
indiana_jones_stats = {
    'health': 85,
    'speed': coeff,
    'attack': 11,
    'attack_speed': 18,
    'stamina': 95}

adventurer_dico_v1 = {
    'Adventurer/Adventurer_Spritesheet.png' : [[7],[6,8,9,4,7,9,6]]}
adventurer_data = ([7,11],[12,20], 6, 14)
adventurer_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2,5],
    'Hit' : [3],
    'Death' : [4]}
adventurer_stats = {
    'health': 75,
    'speed': coeff*4/3,
    'attack': 8,
    'attack_speed': 27,
    'stamina': 150}

bat_dico_v1 = {
    'Bat/Bat_SpriteSheet.png' : [[3],[5,5,5]]}
bat_data = ([5,5],[6,6], 0, 0)
bat_indexs = {
    'Idle' : [0],
    'Walk' : [0],
    'Attack' : [0],
    'Hit' : [1],
    'Death' : [2]}
bat_stats = {
    'health': 1,
    'speed': coeff*4/3,
    'attack': 0,
    'attack_speed': 1,
    'stamina': 0}

halo_dico_v1 = {
    'Halo/Halo_Sprite_Sheet.png' : [[5],[4,8,5,3,9]]}
halo_data = ([11,8],[10,21],0, 35)
halo_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2],
    'Hit' : [3],
    'Death' : [4]}
halo_stats = {
    'health': 92,
    'speed': coeff,
    'attack': 10,
    'attack_speed': 23,
    'stamina': 105}

gladiator_dico_v1 = {
    'Gladiator/Gladiator_Spritesheet.png' : [[5],[5,8,7,3,7]]}
gladiator_data = ([11,7],[10,24],0, 13)
gladiator_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2],
    'Hit' : [3],
    'Death' : [4]}
gladiator_stats = {
    'health': 90,
    'speed': coeff,
    'attack': 14,
    'attack_speed': 17,
    'stamina': 120}

demon_dico_v1 = {
    'Demon/demon_spritesheet.png' : [[4], [6,6,4,8]]}
demon_data = ([25,20],[27,32],-13, 5)
demon_indexs = {
    'Idle' : [0],
    'Walk' : [0],
    'Attack' : [1],
    'Hit' : [2],
    'Death' : [3]}
demon_stats = {
    'health': 150,
    'speed': coeff,
    'attack': 75,
    'attack_speed': 13,
    'stamina': 130}

cyclop_dico_v1 = {
    'Cyclop/Cyclop_Spritesheet.png' : [[10],[15,12,5,8,3,5,9,8,6,8]]}
cyclop_data = ([22,20],[18,34],2, 26)
cyclop_indexs = {
    'Idle' : [0,0,0,0,7],
    'Walk' : [1],
    'Attack' : [2,2,2,3],
    'Hit' : [5],
    'Death' : [6],
    'Laser attack' : [7],
    'Laser beam': [8]}
cyclop_stats = {
    'health': 275,
    'speed': coeff*2/3,
    'attack': 16,
    'attack_speed': 16,
    'stamina': 175}

hobbit_dico_v2 = {
    'Hobbit/' : [[8], [7,13,12,4,4,10,10,8]]}
hobbit_data = ([26,22],[12,17],0, 28)
hobbit_indexs = {
    'Idle' : [4],
    'Walk' : [6],
    'Attack' : [0],
    'Hit' : [3],
    'Death' : [2]}
hobbit_stats = {
    'health': 75,
    'speed': coeff*4/3,
    'attack': 8,
    'attack_speed': 26,
    'stamina': 60}

question_mark_dico_v2 = {
    'Question_mark/' : [[2], [6,8]]}
question_mark_data = ([6,3],[19,30],0, 20)
question_mark_indexs = {
    'Idle' : [0],
    'Attack' : [1]}
question_mark_stats = {}


heroes_dico = {
    'santa' : [0, santa_data, santa_indexs, santa_stats],
    'minotaur' : [1, minotaur_data, minotaur_indexs, minotaur_stats],
    'dwarf' : [2, dwarf_data, dwarf_indexs, dwarf_stats],
    'indiana_jones' : [3, indiana_jones_data, indiana_jones_indexs, indiana_jones_stats],
    'adventurer' : [4, adventurer_data, adventurer_indexs, adventurer_stats],
    'bat' : [5, bat_data, bat_indexs, bat_stats],
    'halo' : [6, halo_data, halo_indexs, halo_stats],
    'gladiator' : [7, gladiator_data, gladiator_indexs, gladiator_stats],
    'demon' : [8, demon_data, demon_indexs, demon_stats],
    'cyclop' : [9, cyclop_data, cyclop_indexs, cyclop_stats],
    'hobbit' : [10, hobbit_data, hobbit_indexs, hobbit_stats],
    'question_mark' : [11, question_mark_data, question_mark_indexs, question_mark_stats]}