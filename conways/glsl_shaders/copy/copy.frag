#version 330 core

layout (location = 0) out vec4 fragColor;
uniform sampler2D state;
uniform vec2 scale;

void main() {
    fragColor = texture(state, gl_FragCoord.xy / scale);

}
