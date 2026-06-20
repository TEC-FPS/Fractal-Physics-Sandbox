TEC-FPS is an open-source Fractal Physics Sandbox dedicated to developing dynamic environments that allow for organically emerging functions. 
It is currently (and forever will be) free to download in the official TEC-FPS Discord (https://discord.gg/TyYwbefE). 


-----------------Current Features-----------------------

Layer 1: This layer starts with two "nodes" spawning in a random location in a fluid matrix. They populate based on the energy in the system, and "scar" their environment to create a basic form of memory. 
They have no borders, they travel in a 3D Torus on a 2D surface, and there is always a small amount of energy being pumped into their environment in the direction of South East. 
This "pumping" of energy causes the fluid to constantly shift, which deforms the nodes previous tracks, ensuring the "scarring" is not falsely permanent. 
Users in this layer can press TAB to display sliders, which allow for tweaking values like energy intake, cost of movement, steering sensitivity, cost to reproduce, fluid density etc.
Pressing SPACE BAR brings up a small window in the top right of your screen, this window is mostly meant for Layer 2 but still functions in Layer 1. 
Additionally, the system is connected to the CPU and its internal clock, interactions with the program will cause a disruption in their environment and "kill" the weakest nodes, whether they are weak due to low battery, 
bad positioning, excessive exterior pressures, or any mix of. Once users have established a Layer 1 they are happy with, or if they prefer to keep the values at their starting positions, 
they can press 2 on their keyboard at anytime to active Layer 2.

Layer 2: Layer 2 starts by spawning two bodies near the center of the fluid matrix at a specific distance from one another (this currently does not change but may in the future). 
The fluid they are in is currently dark, as it does not carry any energy. Additionally, there is no flow of energy in this layer from any direction, this layer does not have "food" at this point (currently in development). 
It also does not have organic reproduction like the Layer 1 nodes do (currently in development). The bodies in Layer 2 can be clicked on and highlighted, and this is where SPACE BAR finally shines. 
Each body in Layer 2 comes with its own Layer 1 inside of them, the first two bodies have identical copies of their Layer 1 but only at the beginning. 
As they interact with other bodies their insides will change according to their individual existence. User can press M and spawn another body, which has its own Layer 1 inside. 
SPACE BAR brings up a window that is a live feed inside any body you highlight, there is no limit to how many bodies you can currently spawn. As they travel in this dark fluid, 
they travel based on the vector directions and velocity of the Layer 1 nodes that are inside of it. Layer 2 bodies move because of their Layer 1 nodes, 
the way Layer 1 nodes move is due to the environment and interactions of the Layer 2 bodies. Layer 1 has no physical borders, it remains a Torus, but because it lives inside a Layer 2 body, 
its forced to behave in a certain way. Users can also press TAB on any Layer 2 body and change their Layer 1 values. As these bodies travel you will notice they leave a cool looking glowing pattern that eventually lights up the fluid, 
this is not a visual design choice. It is a direct results of the Layer 1 nodes bleeding energy as they push the Layer 2 bodies around, and since there is no energy in Layer 2s fluid, that is where the "light" comes from. 
Since there is no "food" in Layer 2, the bodies eventually die depending on how eventful their existence was. Tweaking their values can make Layer 2 bodies last almost indefinitely, and pressing M will always spawn more.
