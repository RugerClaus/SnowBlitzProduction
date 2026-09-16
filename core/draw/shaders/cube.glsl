#version 330 core

layout(location = 0) in vec3 position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float time;

void main()
{
    float angle = time;

    mat3 rotation = mat3(
        cos(angle),  0.0, sin(angle),
        0.0,         1.0, 0.0,
        -sin(angle), 0.0, cos(angle)
    );

    vec3 rotated_position = rotation * position;

    gl_Position =
        projection *
        view *
        model *
        vec4(rotated_position, 1.0);
}