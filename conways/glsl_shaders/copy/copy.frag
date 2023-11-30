#version 330 core
// not my code. copied from the excelent repo https://github.com/skeeto/webgl-game-of-life/
layout (location = 0) out vec4 fragColor;
uniform sampler2D state;
uniform vec2 scale;

void main() {
    fragColor = texture(state, gl_FragCoord.xy / scale);

}
