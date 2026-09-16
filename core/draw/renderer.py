from OpenGL import GL as gl
from helper import asset
from core.draw.camera import Camera3D
from core.draw.shader import Shader

class Renderer:

    def __init__(self, window, resolution=(1600, 900)):
        self.window = window
        self.resolution = resolution
        self.camera = Camera3D()

        self.default_shader = Shader(
            asset("v"),
            asset("f")
        )

        self.texture_shader = Shader(
            asset("texturev"),
            asset("texturef")
        )

        self.initialize_opengl()

    def set_res(self, resolution):
        self.resolution = resolution

    def shader(self, vertex_filename, fragment_filename):
        return Shader(vertex_filename, fragment_filename)

    def update_viewport(self):
        width, height = self.window.size
        gl.glViewport(0, 0, width, height)

    def render_2d(self, object, shader, time):
        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glUniform4f(shader.color_location, *object.color)
        gl.glUniform1f(shader.time_location, time)

    def render_3d(self, object, shader, time):
        gl.glEnable(gl.GL_DEPTH_TEST)

        gl.glUniform4f(shader.color_location, *object.color)
        gl.glUniform1f(shader.time_location, time)

        gl.glUniformMatrix4fv(
            shader.model_location,
            1,
            gl.GL_TRUE,
            object.model_matrix()
        )

        gl.glUniformMatrix4fv(
            shader.view_location,
            1,
            gl.GL_TRUE,
            self.camera.view_matrix()
        )

        gl.glUniformMatrix4fv(
            shader.projection_location,
            1,
            gl.GL_TRUE,
            self.camera.projection_matrix(
                self.window.size[0] / self.window.size[1]
            )
        )

    def render_texture(self, object, shader, time):

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glUniform1f(shader.time_location, time)

        gl.glActiveTexture(gl.GL_TEXTURE0)

        gl.glBindTexture(
            gl.GL_TEXTURE_2D,
            object.texture.id
        )

        gl.glUniform1i(
            shader.texture_location,
            0
        )

    def render(self, object, time):
        shader = object.shader or self.default_shader

        gl.glUseProgram(shader.program)

        if getattr(object, "texture", None):
            self.render_texture(object, shader, time)

        elif object.dimension == 2:
            self.render_2d(object, shader, time)

        elif object.dimension == 3:
            self.render_3d(object, shader, time)

        gl.glBindVertexArray(object.vao)
        gl.glDrawElements(gl.GL_TRIANGLES,object.vertex_count,gl.GL_UNSIGNED_INT,None)

    def clear(self, color=(0.0, 0.0, 0.0, 1.0)):
        width, height = self.window.size
        gl.glViewport(0, 0, width, height)

        gl.glClearColor(*color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def initialize_opengl(self):
        gl.glEnable(gl.GL_DEPTH_TEST)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(
            gl.GL_SRC_ALPHA,
            gl.GL_ONE_MINUS_SRC_ALPHA
        )