#data = [(offset_x,offset_y),(hitbox_w,hitbox_h), flip_offset]

santa_dico_v1 = {
    'Santa/Santa_SpriteSheet.png' : [[22], [5,8,5,5,6,9,8,6,5,4,7,1,1,1,1,1,1,1,1,1,1,1]]}
santa_data = ([3,35],[19,29], 71)
santa_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2,2],
    'Hit' : [9],
    'Death' : [10]}


minotaur_dico_v1 = {
    'Minotaur/Minotaur_Spritesheet.png' : [[10],[5,8,5,9,5,6,9,3,3,6]]}
minotaur_data = ([32,24],[30,34],1)
minotaur_indexs = {
    'Idle' : [0,0,0,2,2,5],
    'Walk' : [1],
    'Attack' : [3,4,6],
    'Hit' : [8],
    'Death' : [9]}


dwarf_dico_v1 = {
    'Dwarf/Dwarf_SpriteSheet.png' : [[8],[5,8,7,6,2,5,4,7]]}
dwarf_data = ([26,10],[11,19],1)
dwarf_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2,3,4],
    'Hit' : [6],
    'Death' : [7]}



indiana_jones_dico_v1 = {
    'Indiana_Jones/Indiana_Jones_SpriteSheet.png' : [[7],[8,8,7,6,8,4,5]]}
indiana_jones_data = ([26,10],[11,22],1)
indiana_jones_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [3,3,4,4,5],
    'Hit' : [5],
    'Death' : [6]}


adventurer_dico_v1 = {
    'Adventurer/Adventurer_Spritesheet.png' : [[7],[6,8,9,4,7,9,6]]}
adventurer_data = ([7,11],[12,20], 6)
adventurer_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2,5],
    'Hit' : [3],
    'Death' : [4]}


bat_dico_v1 = {
    'Bat/Bat_SpriteSheet.png' : [[3],[5,5,5]]}
bat_data = ([5,5],[6,6], 0)
bat_indexs = {
    'Idle' : [0],
    'Walk' : [0],
    'Attack' : [0],
    'Hit' : [1],
    'Death' : [2]}


halo_dico_v1 = {
    'Halo/Halo_Sprite_Sheet.png' : [[5],[4,8,5,3,8]]}
halo_data = ([11,8],[10,21],0)
halo_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2],
    'Hit' : [3],
    'Death' : [4]}


gladiator_dico_v1 = {
    'Gladiator/Gladiator_Spritesheet.png' : [[5],[5,8,7,3,7]]}
gladiator_data = ([11,7],[10,24],0)
gladiator_indexs = {
    'Idle' : [0],
    'Walk' : [1],
    'Attack' : [2],
    'Hit' : [3],
    'Death' : [4]}


demon_dico_v1 = {
    'Demon/demon_spritesheet.png' : [[4], [6,6,4,8]]}
demon_data = ([25,20],[27,32],-13)
demon_indexs = {
    'Idle' : [0],
    'Walk' : [0],
    'Attack' : [1],
    'Hit' : [2],
    'Death' : [3]}


cyclop_dico_v1 = {
    'Cyclop/Cyclop_Spritesheet.png' : [[10],[15,12,7,13,3,5,9,8,6,8]]}
cyclop_data = ([22,20],[18,34],2)
cyclop_indexs = {
    'Idle' : [0,0,0,0,7],
    'Walk' : [1],
    'Attack' : [2,2,2,3],
    'Hit' : [5],
    'Death' : [6],
    'Laser attack' : [7],
    'Laser beam': [8]}


hobbit_dico_v2 = {
    'Hobbit/' : [[8], [17,13,12,4,4,10,10,8]]}
hobbit_data = ([26,22],[12,17],0)
hobbit_indexs = {
    'Idle' : [4],
    'Walk' : [6],
    'Attack' : [0],
    'Hit' : [3],
    'Death' : [2],}


# skeleton buggué
skeleton_dico_v3 = {
    'Skeleton/Skeleton_Hit.png':8,
    'Skeleton/Skeleton_Idle.png':11,
    'Skeleton/Skeleton_Walk.png':13,
    'Skeleton/Skeleton_Dead.png':15,
    'Skeleton/Skeleton_Attack.png':18,
    'Skeleton/Skeleton_React.png':4}
skeleton_data = ([10,13],[12,25],6)
skeleton_indexs = {
    'Idle' : [1,1,1,5],
    'Walk' : [2],
    'Attack' : [4],
    'Hit' : [0],
    'Death' : [3],}



heroes_dico = {
    'santa' : [0,santa_data,santa_indexs],
    'minotaur' : [1,minotaur_data,minotaur_indexs],
    'dwarf' : [2,dwarf_data,dwarf_indexs],
    'indiana_jones' : [3,indiana_jones_data,indiana_jones_indexs],
    'adventurer' : [4,adventurer_data, adventurer_indexs],
    'bat' : [5,bat_data,bat_indexs],
    'halo' : [6,halo_data,halo_indexs],
    'gladiator' : [7,gladiator_data,gladiator_indexs],
    'demon' : [8,demon_data, demon_indexs],
    'cyclop' : [9,cyclop_data, cyclop_indexs],
    'hobbit' : [10,hobbit_data,hobbit_indexs],
    'skeleton' : [11,skeleton_data,skeleton_indexs]}