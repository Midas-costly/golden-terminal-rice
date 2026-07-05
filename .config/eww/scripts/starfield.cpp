#include <gtk/gtk.h>
#include <gtk-layer-shell/gtk-layer-shell.h>
#include <epoxy/gl.h>
#include <vector>
#include <cmath>
#include <random>

struct Particle {
    float r;
    float angle;
    float size;
    float r_col, g_col, b_col;
};

std::vector<Particle> particles;
GLuint vao, vbo, shader_program;
float u_time = 0.0f;

const char* vertex_shader_source = R"glsl(
#version 330 core
layout (location = 0) in float aRadius;
layout (location = 1) in float aAngle;
layout (location = 2) in float aSize;
layout (location = 3) in vec3 aColor;

uniform float u_time;
uniform vec2 u_resolution;
out vec3 vColor;

void main() {
    float current_angle = aAngle - u_time * 0.2; 
    
    // Calculate raw X and Z coordinates on a flat plane
    float x = aRadius * cos(current_angle);
    float z = aRadius * sin(current_angle);
    
    // THE CINEMATIC SWAY
    // Oscillates the viewing angle smoothly between edge-on and top-down
    float tilt_factor = 0.55 + sin(u_time * 0.15) * 0.40; 
    float y = z * tilt_factor; 
    
    // Zoom factor to keep the crisp, vast aesthetic
    float zoom = 1.35;
    vec2 ndc = vec2(x / (u_resolution.x / (2.0 * zoom)), y / (u_resolution.y / (2.0 * zoom)));
    gl_Position = vec4(ndc, 0.0, 1.0);
    
    // TRUE 3D DEPTH ILLUSION
    // Scale size based on Z-depth (stars in front are larger, stars in back shrink)
    float depth_scale = 1.0 + (z / 1500.0); 
    gl_PointSize = aSize * 1.2 * depth_scale; 
    
    // Fade stars slightly as they recede into the distance
    float depth_fade = 1.0 + (z / 1000.0);
    vColor = aColor * clamp(depth_fade, 0.35, 1.5);
}
)glsl";

const char* fragment_shader_source = R"glsl(
#version 330 core
in vec3 vColor;
out vec4 FragColor;

void main() {
    vec2 coord = gl_PointCoord - vec2(0.5);
    float dist = length(coord);
    if(dist > 0.5) discard; 
    
    // Crisp spheres for the vast space aesthetic
    float alpha = smoothstep(0.5, 0.35, dist);
    vec3 brightColor = vColor * 1.5;
    FragColor = vec4(brightColor * alpha, alpha);
}
)glsl";

GLuint compile_shader(GLenum type, const char* source) {
    GLuint shader = glCreateShader(type);
    glShaderSource(shader, 1, &source, NULL);
    glCompileShader(shader);
    return shader;
}

void generate_galaxy() {
    int num_arms = 2;
    float core_radius = 120.0f;
    float galaxy_radius = 650.0f;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<float> d_core(0.0f, core_radius * 0.4f);
    std::uniform_real_distribution<float> d_theta(0.0f, 2.0f * M_PI);
    std::uniform_real_distribution<float> d_r(20.0f, galaxy_radius);

    float r_col = 229.0f / 255.0f;
    float g_col = 169.0f / 255.0f;
    float b_col = 26.0f / 255.0f;

    for (int i = 0; i < 2500; ++i) {
        float r = std::abs(d_core(gen));
        float theta = d_theta(gen);
        float size = 1.5f + (gen() % 100) / 100.0f; 
        particles.push_back({r, theta, size, r_col, g_col, b_col});
    }

    for (int i = 0; i < 5000; ++i) {
        float r = d_r(gen);
        float arm_offset = ((gen() % num_arms) * 2.0f * M_PI) / num_arms;
        float base_theta = arm_offset + (r * 0.015f);
        
        std::normal_distribution<float> d_noise(0.0f, 0.3f + (r / galaxy_radius) * 0.8f);
        float theta = base_theta + d_noise(gen);
        
        float intensity = 1.0f - (r / galaxy_radius);
        float size = 0.8f + intensity * 1.5f; 
        
        particles.push_back({r, theta, size, r_col * intensity, g_col * intensity, b_col * intensity});
    }
}

gboolean update_clock(gpointer user_data) {
    u_time += 0.016f; 
    gtk_widget_queue_draw(GTK_WIDGET(user_data)); 
    return G_SOURCE_CONTINUE;
}

static void on_realize(GtkGLArea *area) {
    gtk_gl_area_make_current(area);
    glEnable(GL_PROGRAM_POINT_SIZE); 
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE); 

    GLuint vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_shader_source);
    GLuint fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_source);
    
    shader_program = glCreateProgram();
    glAttachShader(shader_program, vertex_shader);
    glAttachShader(shader_program, fragment_shader);
    glLinkProgram(shader_program);
    
    generate_galaxy();

    glGenVertexArrays(1, &vao);
    glGenBuffers(1, &vbo);
    
    glBindVertexArray(vao);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, particles.size() * sizeof(Particle), particles.data(), GL_STATIC_DRAW);

    glVertexAttribPointer(0, 1, GL_FLOAT, GL_FALSE, sizeof(Particle), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, sizeof(Particle), (void*)(sizeof(float)));
    glEnableVertexAttribArray(1);
    glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, sizeof(Particle), (void*)(2 * sizeof(float)));
    glEnableVertexAttribArray(2);
    glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, sizeof(Particle), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(3);
}

static gboolean on_render(GtkGLArea *area, GdkGLContext *context) {
    int width = gtk_widget_get_allocated_width(GTK_WIDGET(area));
    int height = gtk_widget_get_allocated_height(GTK_WIDGET(area));

    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    glUseProgram(shader_program);
    glUniform1f(glGetUniformLocation(shader_program, "u_time"), u_time);
    glUniform2f(glGetUniformLocation(shader_program, "u_resolution"), (float)width, (float)height);

    glBindVertexArray(vao);
    glDrawArrays(GL_POINTS, 0, particles.size());

    return TRUE;
}

static void activate(GtkApplication* app, gpointer user_data) {
    GtkWidget *window = gtk_application_window_new(app);
    
    gtk_widget_set_app_paintable(window, TRUE);
    GdkScreen *screen = gtk_widget_get_screen(window);
    GdkVisual *visual = gdk_screen_get_rgba_visual(screen);
    if (visual != NULL && gdk_screen_is_composited(screen)) {
        gtk_widget_set_visual(window, visual);
    }

    gtk_layer_init_for_window(GTK_WINDOW(window));
    gtk_layer_set_layer(GTK_WINDOW(window), GTK_LAYER_SHELL_LAYER_BOTTOM);
    gtk_layer_set_namespace(GTK_WINDOW(window), "ghost-starfield");
    
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_TOP, TRUE);
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_RIGHT, TRUE);
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_BOTTOM, TRUE);
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_LEFT, FALSE);
    
    gtk_layer_set_margin(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_TOP, 2);
    gtk_layer_set_margin(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_RIGHT, 2);
    gtk_layer_set_margin(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_BOTTOM, 2);

    GtkCssProvider *css_provider = gtk_css_provider_new();
    gtk_css_provider_load_from_data(css_provider, "box { border: 1px solid #E5A91A; padding: 2px; background-color: #000000; }", -1, NULL);
    gtk_style_context_add_provider_for_screen(screen, GTK_STYLE_PROVIDER(css_provider), GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);

    GtkWidget *box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 0);
    gtk_container_add(GTK_CONTAINER(window), box);

    GtkWidget *gl_area = gtk_gl_area_new();
    gtk_gl_area_set_has_alpha(GTK_GL_AREA(gl_area), TRUE);
    gtk_widget_set_size_request(gl_area, 1075, 1063);
    gtk_box_pack_start(GTK_BOX(box), gl_area, TRUE, TRUE, 0);

    g_signal_connect(gl_area, "realize", G_CALLBACK(on_realize), NULL);
    g_signal_connect(gl_area, "render", G_CALLBACK(on_render), NULL);

    g_timeout_add(16, update_clock, gl_area);

    gtk_widget_show_all(window);
}

int main(int argc, char **argv) {
    GtkApplication *app = gtk_application_new("com.ghost.starfield", G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    int status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);
    return status;
}
