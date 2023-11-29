#version 330 core
// Not my code. copied from this great repo https://github.com/skeeto/webgl-game-of-life/ 
layout (location = 0) out vec4 fragColor;

uniform sampler2D state;
uniform vec2 scale;

int get(int x, int y) {
    return int(texture(state, (gl_FragCoord.xy + vec2(x, y)) / scale).r);
}

void main() {
    int sum = get(-1, -1) +
              get(-1,  0) +
              get(-1,  1) +
              get( 0, -1) +
              get( 0,  1) +
              get( 1, -1) +
              get( 1,  0) +
              get( 1,  1);
    if (sum == 3) {
        fragColor = vec4(1.0, 1.0, 1.0, 1.0);
    } else if (sum == 2) {
        float current = float(get(0, 0));
        fragColor = vec4(current, current, current, 1.0);
    } else {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    } 
}

