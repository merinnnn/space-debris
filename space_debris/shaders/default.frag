#version 330 core

layout (location = 0) out vec4 fragColour;

void main() {
    vec3 colour = vec3(1, 0, 0);
    fragColour = vec4(colour, 1.0);

}