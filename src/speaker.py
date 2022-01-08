# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Connect Grove cable to pin 0

from microbit import speaker, set_volume, sleep
import music

jingle_bells = [
    'e:2', 'e:2', 'e:4',
    'e:2', 'e:2', 'e:4',
    'e:2', 'g:2', 'c', 'd',
    'e:8', 'f:2', 'f:2', 'f:3',
    'f:1', 'f:2', 'e:2',
    'e:2', 'e:1', 'e:1',
    'e:2', 'd:2', 'd:2',
    'e:2', 'd:4', 'g:4',
    'e:2', 'e:2', 'e:4',
    'e:2', 'e:2', 'e:4',
    'e:2', 'g:2', 'c', 'd',
    'e:8', 'f:2', 'f:2', 'f:2',
    'f:2', 'f:2', 'e:2',
    'e:2', 'e:1', 'e:1',
    'g:2', 'g:2', 'f:2',
    'd:2', 'c:4'
    ]

silent_night = [
    'R:20',
    'g4:6', 'a4:2', 'g4:4', 'e4:12', 'g4:6',
    'a4:2', 'g4:4', 'e4:12',
    'd5:8', 'd5:4', 'b4:8',
    'b4:4', 'c5:8', 'c5:4', 'g4:12'
    'a4:8', 'a4:4', 'c5:6', 'b4:2',
    'a4:4', 'g4:6', 'a4:2', 'g4:4', 'e4:8', 'g4:4',
    'a4:8', 'a4:4', 'c5:6', 'b4:2', 'a4:4', 'g4:6'
    'a4:2', 'g4:4', 'e4:8', 'g4:4',
    'd5:8', 'd5:4', 'f5:6', 'd5:2', 'b4:4', 'c5:12',
    'e5:4', 'r:8', 'c5:6', 'g4:2', 'e4:4', 'g4:6',
    'f4:2', 'd4:4', 'c4:16', 'r:8'
    ]

we_wish_you_a_merry_christmas = [
    'R:20',
    'a5:2', 'd6:4', 'd6:2', 'e6:2',
    'd6:2', 'c#6:2', 'b5:4', 'g5:4', 'b5:2',
    'e6:4', 'e6:2', 'f#6:2', 'e6:2', 'd6:2',
    'c#6:4', 'a5:4', 'c#6:2', 'f#6:4', 'f#6:2',
    'g6:2', 'f#6:2', 'e6:2', 'd6:4', 'b5:4',
    'a5:2', 'b5:2', 'e6:2', 'c#6:2', 'd6:2', 'R:4'
    ]

speaker.off()
set_volume(255)

music.set_tempo(ticks=4, bpm=120)

for i in range(4):
    print("Loop:", i)
    
    print("Now playing: Jingle Bells...")
    music.play(jingle_bells)
    sleep(2000)
    
    print("Now playing: Silent Night...")
    music.play(silent_night)
    sleep(2000)

    print("Now playing: We wish you a merry Christmas...")
    music.play(we_wish_you_a_merry_christmas)
    sleep(2000)

speaker.on()
