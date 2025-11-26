import os
import sys
import ctypes
from typing import Optional, Tuple, List

try:
    import customtkinter as ctk
except Exception:
    ctk = None

try:
    from PIL import Image, ImageTk, ImageDraw
except Exception:
    Image = None
    ImageTk = None
    ImageDraw = None

import tkinter as tk
from tkinter import messagebox


def resource_path(filename: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


class RouterLib:
    """Wrapper to load a C library that provides route generation."""

    def __init__(self):
        self.lib = None
        self._load_lib()

    def _load_lib(self):
        candidates = [
            resource_path('backend\\router.dll'),
            resource_path('backend\\librouter.dll'),
            resource_path('router.dll'),
            resource_path('librouter.dll'),
            resource_path('librouter.so'),
            resource_path('librouter.dylib'),
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    self.lib = ctypes.CDLL(path)
                    if hasattr(self.lib, 'generate_route'):
                        self.lib.generate_route.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
                        self.lib.generate_route.restype = ctypes.c_int
                    
                    # Configurar função de teste
                    if hasattr(self.lib, 'get_test_message'):
                        self.lib.get_test_message.argtypes = []
                        self.lib.get_test_message.restype = ctypes.c_char_p
                    
                    # Configurar funções para obter pontos turísticos
                    if hasattr(self.lib, 'get_num_pontos'):
                        self.lib.get_num_pontos.argtypes = []
                        self.lib.get_num_pontos.restype = ctypes.c_int
                    
                    if hasattr(self.lib, 'get_ponto_info'):
                        self.lib.get_ponto_info.argtypes = [
                            ctypes.c_int,           # index
                            ctypes.c_char_p,        # nome_out
                            ctypes.c_int,           # nome_len
                            ctypes.c_char_p,        # categoria_out
                            ctypes.c_int,           # cat_len
                            ctypes.POINTER(ctypes.c_int)  # id_out
                        ]
                        self.lib.get_ponto_info.restype = ctypes.c_int
                    
                    return
                except Exception:
                    self.lib = None

    def get_test_message(self) -> str:
        """Obtém mensagem de teste do backend C"""
        if self.lib and hasattr(self.lib, 'get_test_message'):
            try:
                result = self.lib.get_test_message()
                if result:
                    return result.decode('utf-8', errors='ignore')
            except Exception as e:
                return f'Erro ao chamar C: {e}'
        return '⚠️ Biblioteca C não carregada (usando simulação Python)'

    def load_tourist_spots(self) -> dict:
        """Carrega pontos turísticos do backend C"""
        spots = {}
        
        if not self.lib or not hasattr(self.lib, 'get_num_pontos') or not hasattr(self.lib, 'get_ponto_info'):
            return spots
        
        try:
            num_pontos = self.lib.get_num_pontos()
            
            for i in range(num_pontos):
                nome_buf = ctypes.create_string_buffer(100)
                cat_buf = ctypes.create_string_buffer(30)
                id_val = ctypes.c_int()
                
                result = self.lib.get_ponto_info(i, nome_buf, 100, cat_buf, 30, ctypes.byref(id_val))
                
                if result == 0:
                    nome = nome_buf.value.decode('utf-8', errors='ignore')
                    id_ponto = id_val.value
                    # Usar o ID como coordenada (x, y)
                    spots[nome] = (id_ponto, id_ponto)
        
        except Exception as e:
            print(f"Erro ao carregar pontos turísticos: {e}")
        
        return spots

    def generate_route(self, sx: int, sy: int, ex: int, ey: int) -> str:
        if self.lib and hasattr(self.lib, 'generate_route'):
            buf_len = 8192
            buf = ctypes.create_string_buffer(buf_len)
            try:
                res = self.lib.generate_route(int(sx), int(sy), int(ex), int(ey), buf, buf_len)
                if res == 0:
                    return buf.value.decode('utf-8', errors='ignore')
                else:
                    return f'% (C lib returned code {res})'
            except Exception as e:
                return f'C library call failed: {e}'

        # Fallback simulation
        steps = max(2, int(max(abs(ex - sx), abs(ey - sy)) / 20))
        pts = []
        for i in range(steps + 1):
            t = i / steps
            x = int(sx + (ex - sx) * t)
            y = int(sy + (ey - sy) * t)
            pts.append((x, y))
        return '\n'.join(f'{x},{y}' for x, y in pts)


class StartScreen:
    def __init__(self):
        if ctk:
            ctk.set_appearance_mode('Dark')
            ctk.set_default_color_theme('blue')
            self.root = ctk.CTk()
            self.is_ctk = True
        else:
            self.root = tk.Tk()
            self.is_ctk = False

        self.root.title('Navigation System')
        self.root.geometry('600x400')
        self.root.minsize(500, 300)
        self.root.configure(bg='#1a1a1a')
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        self.app_instance = None
        self._build_ui()

    def _build_ui(self):
        # Main container
        if self.is_ctk:
            main_frame = ctk.CTkFrame(self.root, fg_color='transparent')
            main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        else:
            main_frame = tk.Frame(self.root, bg='#1a1a1a')
            main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        # Title
        title_font = ('Arial', 28, 'bold')
        if self.is_ctk:
            title = ctk.CTkLabel(main_frame, text="🚀 Navigation System", 
                               font=title_font, text_color="#4cc9f0")
            title.pack(pady=(0, 10))
            
            subtitle = ctk.CTkLabel(main_frame, text="Sistema de Geração de Rotas", 
                                  font=('Arial', 14), text_color="#888888")
            subtitle.pack(pady=(0, 40))
        else:
            title = tk.Label(main_frame, text="🚀 Navigation System", 
                           font=title_font, bg='#1a1a1a', fg='#4cc9f0')
            title.pack(pady=(0, 10))
            
            subtitle = tk.Label(main_frame, text="Sistema de Geração de Rotas", 
                              font=('Arial', 14), bg='#1a1a1a', fg='#888888')
            subtitle.pack(pady=(0, 40))

        # Mode selection buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color='transparent') if self.is_ctk else tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(expand=True, fill='both')

        # Multi-destination route button
        if self.is_ctk:
            multi_btn = ctk.CTkButton(button_frame, 
                                    text="🗺️ Criar Rota\n(Múltiplos Destinos)",
                                    font=('Arial', 16, 'bold'),
                                    height=80,
                                    fg_color="#4361ee",
                                    hover_color="#3a56d4",
                                    command=lambda: self.start_app(True))
            multi_btn.pack(fill='x', pady=10)
            
            single_btn = ctk.CTkButton(button_frame,
                                     text="📍 Ir a um Ponto\n(Apenas um Destino)", 
                                     font=('Arial', 16, 'bold'),
                                     height=80,
                                     fg_color="#f72585",
                                     hover_color="#df2277",
                                     command=lambda: self.start_app(False))
            single_btn.pack(fill='x', pady=10)
        else:
            multi_btn = tk.Button(button_frame,
                                text="🗺️ Criar Rota\n(Múltiplos Destinos)",
                                font=('Arial', 14, 'bold'),
                                bg='#4361ee',
                                fg='white',
                                relief='flat',
                                height=4,
                                command=lambda: self.start_app(True))
            multi_btn.pack(fill='x', pady=10)
            
            single_btn = tk.Button(button_frame,
                                 text="📍 Ir a um Ponto\n(Apenas um Destino)",
                                 font=('Arial', 14, 'bold'),
                                 bg='#f72585',
                                 fg='white',
                                 relief='flat',
                                 height=4,
                                 command=lambda: self.start_app(False))
            single_btn.pack(fill='x', pady=10)

        # Footer
        footer_font = ('Arial', 10)
        if self.is_ctk:
            footer = ctk.CTkLabel(main_frame, text="Sistema Integrado C/Python • v1.0", 
                                font=footer_font, text_color="#666666")
            footer.pack(side='bottom', pady=20)
        else:
            footer = tk.Label(main_frame, text="Sistema Integrado C/Python • v1.0", 
                            font=footer_font, bg='#1a1a1a', fg='#666666')
            footer.pack(side='bottom', pady=20)

    def start_app(self, multi_destination: bool):
        self.root.destroy()
        image_filename = 'perimetro-mapa.png'
        self.app_instance = ModernMapApp(image_filename, multi_destination)
        self.app_instance.run()

    def run(self):
        self.root.mainloop()


class ModernMapApp:
    def __init__(self, image_file: str, multi_destination: bool = True):
        self.image_path = resource_path(image_file)
        self.multi_destination = multi_destination
        
        if not os.path.exists(self.image_path):
            messagebox.showerror('Erro', f'Arquivo não encontrado: {self.image_path}')
            raise SystemExit(1)

        if Image is None or ImageTk is None:
            messagebox.showerror('Dependência ausente', 'Pillow não está instalado. Instale com: pip install pillow')
            raise SystemExit(1)

        # Load image
        self.original_image = Image.open(self.image_path)

        # Router library wrapper
        self.router = RouterLib()

        # UI with modern theme
        if ctk:
            ctk.set_appearance_mode('Dark')
            ctk.set_default_color_theme('blue')
            self.root = ctk.CTk()
            self.is_ctk = True
        else:
            self.root = tk.Tk()
            self.is_ctk = False

        app_title = "Navigation System - "
        app_title += "Rota com Múltiplos Destinos" if multi_destination else "Navegação para um Ponto"
        self.root.title(app_title)
        self.root.geometry('1400x900')
        self.root.minsize(1200, 700)

        # Configure grid for responsive layout
        self.root.grid_columnconfigure(0, weight=0)  # Controls panel
        self.root.grid_columnconfigure(1, weight=1)  # Map area
        self.root.grid_rowconfigure(0, weight=1)

        # State
        self.scale = 1.0
        self.canvas_img_id = None
        self.tk_image = None
        self.origin: Optional[Tuple[int, int]] = None
        self.destinations: List[Tuple[int, int]] = []
        self.markers: List[int] = []
        self.pan_x = 0
        self.pan_y = 0
        self._drag_start = None
        self.route_tags: List[str] = []
        self.route_colors = ['#4cc9f0', '#ffd166', '#ef476f', '#06d6a0', '#118ab2']
        
        # Carregar pontos turísticos do backend C
        self.tourist_spots = self.router.load_tourist_spots() #Por enquanto esta sem coordenadas reais
        
        # Se não conseguiu carregar do C, usar pontos de exemplo
        if not self.tourist_spots:
            self.tourist_spots = {
                "Renner": (270, 338),
                "Ponto de Teste 2": (100, 100),
                "Ponto de Teste 3": (150, 150),
            }

        # Build modern UI
        self._build_modern_ui()

        # Initial render
        self.root.after(100, self._update_canvas_image)

    def _build_modern_ui(self):
        # Left Panel - Controls
        if self.is_ctk:
            self.control_frame = ctk.CTkFrame(self.root, width=380, corner_radius=15)
        else:
            self.control_frame = tk.Frame(self.root, width=380, bg='#2b2b2b')
        
        self.control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.control_frame.grid_propagate(False)

        # Right Panel - Map
        if self.is_ctk:
            self.map_frame = ctk.CTkFrame(self.root, corner_radius=15)
        else:
            self.map_frame = tk.Frame(self.root, bg='#2b2b2b')
        
        self.map_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Configure map frame grid
        self.map_frame.grid_columnconfigure(0, weight=1)
        self.map_frame.grid_rowconfigure(0, weight=1)

        # Create canvas in map frame
        self.canvas = tk.Canvas(self.map_frame, bg='#1a1a1a', highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Build control panel content
        self._build_control_panel()

        # Bind events
        self.canvas.bind('<Button-1>', self._on_canvas_click)
        self.canvas.bind('<ButtonPress-2>', self._on_middle_press)
        self.canvas.bind('<B2-Motion>', self._on_middle_drag)
        self.canvas.bind('<ButtonPress-1>', self._on_left_press)
        self.canvas.bind('<B1-Motion>', self._on_left_drag)
        self.root.bind('<Configure>', self._on_resize)

        self.mode = None

    def _build_control_panel(self):
        # Header with back button and title
        header_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        header_frame.pack(fill='x', padx=15, pady=15)
        
        # Back button
        if self.is_ctk:
            back_btn = ctk.CTkButton(header_frame, text="← Voltar", 
                                   command=self._go_back,
                                   fg_color="transparent",
                                   hover_color="#3b3b3b",
                                   text_color="#4cc9f0",
                                   font=('Arial', 12, 'bold'),
                                   width=80,
                                   height=35)
            back_btn.pack(side='left')
            
            # Title
            title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            title_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))
            
            title = ctk.CTkLabel(title_frame, text="Navigation System", 
                               font=('Arial', 16, 'bold'), text_color="#ffffff")
            title.pack(anchor='center')
            
            mode_text = "Múltiplos Destinos" if self.multi_destination else "Apenas um Destino"
            mode_color = "#4361ee" if self.multi_destination else "#f72585"
            mode_label = ctk.CTkLabel(title_frame, text=f"Modo: {mode_text}", 
                                    font=('Arial', 11), text_color=mode_color)
            mode_label.pack(anchor='center')
        else:
            back_btn = tk.Button(header_frame, text="← Voltar", 
                               command=self._go_back,
                               bg='#2b2b2b', fg='#4cc9f0', font=('Arial', 11, 'bold'),
                               relief='flat', bd=0)
            back_btn.pack(side='left')
            
            title = tk.Label(header_frame, text="Navigation System", 
                           font=('Arial', 14, 'bold'), bg='#2b2b2b', fg='#ffffff')
            title.pack(side='left', padx=(20, 0))

        self._create_separator()

        # Action Buttons Section
        action_font = ('Arial', 12, 'bold')
        if self.is_ctk:
            action_label = ctk.CTkLabel(self.control_frame, text="AÇÕES PRINCIPAIS", 
                                      font=action_font, text_color="#4cc9f0")
            action_label.pack(pady=(15, 5))
        else:
            action_label = tk.Label(self.control_frame, text="AÇÕES PRINCIPAIS", 
                                  font=action_font, bg='#2b2b2b', fg='#4cc9f0')
            action_label.pack(pady=(15, 5))

        # Button container
        btn_container = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        btn_container.pack(fill='x', padx=15, pady=10)

        # Modern buttons with icons
        buttons = [
            ("📍 Marcar Origem", self._set_origin_mode, "#4361ee"),
            ("🎯 Marcar Destino", self._set_dest_mode, "#f72585"),
            ("🚀 Gerar Rota", self._on_generate_route, "#4cc9f0"),
            ("🔌 Testar Backend C", self._test_c_backend, "#06d6a0"),
            ("🗑️ Limpar Tudo", self._clear, "#7209b7"),
        ]

        for text, command, color in buttons:
            if self.is_ctk:
                btn = ctk.CTkButton(btn_container, text=text, command=command,
                                  fg_color=color, hover_color=self._darken_color(color),
                                  height=40, font=('Arial', 12, 'bold'),
                                  corner_radius=8)
                btn.pack(fill='x', pady=4)
            else:
                btn = tk.Button(btn_container, text=text, command=command,
                              bg=color, fg='white', font=('Arial', 11, 'bold'),
                              relief='flat', height=2, bd=0)
                btn.pack(fill='x', pady=4)

        self._create_separator()

        # Pontos Turísticos Section
        if self.is_ctk:
            spots_label = ctk.CTkLabel(self.control_frame, text="PONTOS TURÍSTICOS", 
                                     font=action_font, text_color="#4cc9f0")
            spots_label.pack(pady=(15, 5))
        else:
            spots_label = tk.Label(self.control_frame, text="PONTOS TURÍSTICOS", 
                                 font=action_font, bg='#2b2b2b', fg='#4cc9f0')
            spots_label.pack(pady=(15, 5))

        # Tourist spots buttons
        spots_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        spots_frame.pack(fill='both', expand=True, padx=15, pady=10)

        # Create scrollable frame for tourist spots
        if self.is_ctk:
            scroll_frame = ctk.CTkScrollableFrame(spots_frame, height=200)
            scroll_frame.pack(fill='both', expand=True)
            spots_container = scroll_frame
        else:
            canvas = tk.Canvas(spots_frame, bg='#2b2b2b', highlightthickness=0, height=200)
            scrollbar = tk.Scrollbar(spots_frame, orient='vertical', command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg='#2b2b2b')
            
            scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
            canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            spots_container = scroll_frame

        # Add tourist spot buttons
        for spot_name, coords in self.tourist_spots.items():
            if self.is_ctk:
                spot_btn = ctk.CTkButton(spots_container, text=f"📍 {spot_name}",
                                       command=lambda name=spot_name, c=coords: self._add_tourist_spot(name, c),
                                       fg_color='#3b3b3b',
                                       hover_color='#4a4a4a',
                                       text_color='#ffffff',
                                       font=('Arial', 11),
                                       height=35,
                                       corner_radius=6)
                spot_btn.pack(fill='x', pady=2)
            else:
                spot_btn = tk.Button(spots_container, text=f"📍 {spot_name}",
                                   command=lambda name=spot_name, c=coords: self._add_tourist_spot(name, c),
                                   bg='#3b3b3b', fg='white', font=('Arial', 10),
                                   relief='flat', height=2, anchor='w')
                spot_btn.pack(fill='x', pady=2)

        self._create_separator()

        # Destinations list (only for multi-destination mode)
        if self.multi_destination:
            dest_list_frame = ctk.CTkFrame(self.control_frame) if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
            dest_list_frame.pack(fill='both', padx=15, pady=(5,10))
            
            if self.is_ctk:
                ctk.CTkLabel(dest_list_frame, text='Destinos Marcados:', font=('Arial', 11)).pack(anchor='w', pady=(5,2))
            else:
                tk.Label(dest_list_frame, text='Destinos Marcados:', bg='#2b2b2b', fg='white', font=('Arial', 11)).pack(anchor='w', pady=(5,2))

            # Listbox with modern styling
            listbox_frame = ctk.CTkFrame(dest_list_frame) if self.is_ctk else tk.Frame(dest_list_frame, bg='#1a1a1a')
            listbox_frame.pack(fill='both', expand=True, pady=2)
            
            self.dest_listbox = tk.Listbox(listbox_frame, height=4, bg='#1a1a1a', fg='white', 
                                         selectbackground='#4cc9f0', font=('Arial', 10),
                                         relief='flat', highlightthickness=0)
            self.dest_listbox.pack(fill='both', expand=True, padx=1, pady=1)

            # Modern buttons for destination management
            dbtn_frame = ctk.CTkFrame(dest_list_frame, fg_color='transparent') if self.is_ctk else tk.Frame(dest_list_frame, bg='#2b2b2b')
            dbtn_frame.pack(fill='x', pady=5)
            
            if self.is_ctk:
                remove_btn = ctk.CTkButton(dbtn_frame, text='🗑️ Remover Selecionado', 
                                         command=self._remove_selected_destination,
                                         fg_color='#ef476f', font=('Arial', 11), height=32)
                remove_btn.pack(fill='x', padx=2)
            else:
                remove_btn = tk.Button(dbtn_frame, text='🗑️ Remover Selecionado', 
                                     command=self._remove_selected_destination,
                                     bg='#ef476f', fg='white', font=('Arial', 10), height=2,
                                     relief='flat')
                remove_btn.pack(fill='x', padx=2)

        self._create_separator()

        # Zoom Controls
        if self.is_ctk:
            zoom_label = ctk.CTkLabel(self.control_frame, text="CONTROLES DO MAPA", 
                                    font=action_font, text_color="#4cc9f0")
            zoom_label.pack(pady=(15, 5))
        else:
            zoom_label = tk.Label(self.control_frame, text="CONTROLES DO MAPA", 
                                font=action_font, bg='#2b2b2b', fg='#4cc9f0')
            zoom_label.pack(pady=(15, 5))

        zoom_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        zoom_frame.pack(fill='x', padx=15, pady=10)

        if self.is_ctk:
            ctk.CTkButton(zoom_frame, text="➕ Zoom In", command=self._zoom_in,
                        fg_color="#4361ee", font=('Arial', 12), height=35).pack(side='left', fill='x', expand=True, padx=2)
            ctk.CTkButton(zoom_frame, text="➖ Zoom Out", command=self._zoom_out,
                        fg_color="#f72585", font=('Arial', 12), height=35).pack(side='left', fill='x', expand=True, padx=2)
            ctk.CTkButton(zoom_frame, text="📐 Centralizar", command=self._reset_view,
                        fg_color="#4cc9f0", font=('Arial', 12), height=35).pack(side='left', fill='x', expand=True, padx=2)
        else:
            tk.Button(zoom_frame, text="➕ Zoom In", command=self._zoom_in, 
                    bg="#4361ee", fg='white', font=('Arial', 10), height=2,
                    relief='flat').pack(side='left', fill='x', expand=True, padx=2)
            tk.Button(zoom_frame, text="➖ Zoom Out", command=self._zoom_out, 
                    bg="#f72585", fg='white', font=('Arial', 10), height=2,
                    relief='flat').pack(side='left', fill='x', expand=True, padx=2)
            tk.Button(zoom_frame, text="📐 Centralizar", command=self._reset_view, 
                    bg="#4cc9f0", fg='white', font=('Arial', 10), height=2,
                    relief='flat').pack(side='left', fill='x', expand=True, padx=2)

        # Navigation info
        info_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        info_frame.pack(fill='x', padx=15, pady=5)
        
        info_text = "💡 Dica: Use Ctrl+Arrastar para mover o mapa"
        if self.is_ctk:
            info_label = ctk.CTkLabel(info_frame, text=info_text, font=('Arial', 10), text_color="#888888")
            info_label.pack()
        else:
            info_label = tk.Label(info_frame, text=info_text, font=('Arial', 10), bg='#2b2b2b', fg='#888888')
            info_label.pack()

        self._create_separator()

        # Output/Log Section
        if self.is_ctk:
            log_label = ctk.CTkLabel(self.control_frame, text="LOG DA ROTA", 
                                   font=action_font, text_color="#4cc9f0")
            log_label.pack(pady=(15, 5))
        else:
            log_label = tk.Label(self.control_frame, text="LOG DA ROTA", 
                               font=action_font, bg='#2b2b2b', fg='#4cc9f0')
            log_label.pack(pady=(15, 5))

        # Modern text area with scrollbar
        text_frame = ctk.CTkFrame(self.control_frame) if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        text_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))

        if self.is_ctk:
            self.out_text = ctk.CTkTextbox(text_frame, font=('Consolas', 11), 
                                         fg_color='#1a1a1a', text_color='#00ff88',
                                         scrollbar_button_color='#4cc9f0',
                                         scrollbar_button_hover_color='#3aa8d4')
            self.out_text.pack(fill='both', expand=True, padx=5, pady=5)
        else:
            text_inner_frame = tk.Frame(text_frame, bg='#1a1a1a')
            text_inner_frame.pack(fill='both', expand=True, padx=5, pady=5)
            
            self.out_text = tk.Text(text_inner_frame, font=('Consolas', 10), 
                                  bg='#1a1a1a', fg='#00ff88',
                                  insertbackground='white', wrap='word',
                                  relief='flat')
            scrollbar = tk.Scrollbar(text_inner_frame, orient='vertical', 
                                   command=self.out_text.yview,
                                   bg='#1a1a1a', troughcolor='#2b2b2b')
            self.out_text.configure(yscrollcommand=scrollbar.set)
            
            self.out_text.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')

    def _create_separator(self):
        if self.is_ctk:
            separator = ctk.CTkFrame(self.control_frame, height=2, fg_color="#3b3b3b")
            separator.pack(fill='x', padx=20, pady=10)
        else:
            separator = tk.Frame(self.control_frame, height=2, bg="#3b3b3b")
            separator.pack(fill='x', padx=20, pady=10)

    def _darken_color(self, color, factor=0.8):
        """Darken a hex color for hover effect"""
        if self.is_ctk and color.startswith('#'):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            darkened = tuple(max(0, int(c * factor)) for c in rgb)
            return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
        return color

    def _go_back(self):
        """Voltar para a tela inicial"""
        self.root.destroy()
        start_screen = StartScreen()
        start_screen.run()

    def _test_c_backend(self):
        """Testa a conexão com o backend C"""
        self._log_message("🔌 Testando conexão com backend C...")
        message = self.router.get_test_message()
        self._log_message(f"📨 Resposta do C: {message}")
        messagebox.showinfo("Backend C", message)

    def _set_origin_mode(self):
        self.mode = 'origin'
        self._log_message("🎯 Modo: Marcar Origem - Clique no mapa para definir a origem")

    def _set_dest_mode(self):
        self.mode = 'dest'
        mode_text = "adicionar destino" if self.multi_destination else "definir destino"
        self._log_message(f"🎯 Modo: Marcar Destino - Clique no mapa para {mode_text}")

    def _add_tourist_spot(self, spot_name: str, coords: Tuple[int, int]):
        """Adicionar ponto turístico como destino"""
        x, y = coords
        
        if self.mode == 'origin':
            self.origin = (x, y)
            self._log_message(f"📍 Origem definida: {spot_name} ({x},{y})")
        elif self.mode == 'dest':
            if self.multi_destination:
                self.destinations.append((x, y))
                self._update_dest_listbox()
                self._log_message(f"🎯 {spot_name} adicionado como destino {len(self.destinations)}: ({x},{y})")
            else:
                if self.destinations:
                    self.destinations[0] = (x, y)
                else:
                    self.destinations.append((x, y))
                self._log_message(f"🎯 {spot_name} definido como destino: ({x},{y})")
        else:
            # Se nenhum modo está ativo, perguntar ao usuário
            choice = messagebox.askquestion("Selecionar Tipo", 
                                          f"Deseja adicionar '{spot_name}' como Origem ou Destino?",
                                          icon='question')
            if choice == 'yes':
                self.origin = (x, y)
                self._log_message(f"📍 {spot_name} definido como origem: ({x},{y})")
            else:
                if self.multi_destination:
                    self.destinations.append((x, y))
                    self._update_dest_listbox()
                    self._log_message(f"🎯 {spot_name} adicionado como destino {len(self.destinations)}: ({x},{y})")
                else:
                    if self.destinations:
                        self.destinations[0] = (x, y)
                    else:
                        self.destinations.append((x, y))
                    self._log_message(f"🎯 {spot_name} definido como destino: ({x},{y})")
            
        self._redraw_markers()

    def _log_message(self, message: str):
        self.out_text.insert('end', f"{message}\n")
        self.out_text.see('end')

    def _on_canvas_click(self, event):
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_w, img_h = self.original_image.size
        
        scale = self.scale
        disp_w = int(img_w * scale)
        disp_h = int(img_h * scale)
        x0 = max((canvas_w - disp_w) // 2, 0) + self.pan_x
        y0 = max((canvas_h - disp_h) // 2, 0) + self.pan_y
        
        cx = event.x - x0
        cy = event.y - y0
        if cx < 0 or cy < 0 or cx > disp_w or cy > disp_h:
            return
            
        ix = int(cx / scale)
        iy = int(cy / scale)

        if self.mode == 'origin':
            self.origin = (ix, iy)
            self._log_message(f"📍 Origem definida: {ix},{iy}")
        elif self.mode == 'dest':
            if self.multi_destination:
                self.destinations.append((ix, iy))
                self._update_dest_listbox()
                self._log_message(f"🎯 Destino {len(self.destinations)} adicionado: {ix},{iy}")
            else:
                if self.destinations:
                    self.destinations[0] = (ix, iy)
                else:
                    self.destinations.append((ix, iy))
                self._log_message(f"🎯 Destino definido: {ix},{iy}")
        else:
            self._log_message(f"📌 Coordenadas: {ix},{iy}")
            
        self._redraw_markers()

    def _on_middle_press(self, event):
        self._drag_start = (event.x, event.y, self.pan_x, self.pan_y)

    def _on_middle_drag(self, event):
        if not self._drag_start:
            return
        sx, sy, px, py = self._drag_start
        dx = event.x - sx
        dy = event.y - sy
        self.pan_x = px + dx
        self.pan_y = py + dy
        self._update_canvas_image()

    def _on_left_press(self, event):
        if (event.state & 0x4) != 0:  # Ctrl key
            self._drag_start = (event.x, event.y, self.pan_x, self.pan_y)

    def _on_left_drag(self, event):
        if not self._drag_start:
            return
        sx, sy, px, py = self._drag_start
        dx = event.x - sx
        dy = event.y - sy
        self.pan_x = px + dx
        self.pan_y = py + dy
        self._update_canvas_image()

    def _zoom_in(self):
        self.scale = min(self.scale * 1.2, 5.0)
        self._update_canvas_image()
        self._log_message("🔍 Zoom aumentado")

    def _zoom_out(self):
        self.scale = max(self.scale / 1.2, 0.1)
        self._update_canvas_image()
        self._log_message("🔍 Zoom reduzido")

    def _reset_view(self):
        self.scale = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self._update_canvas_image()
        self._log_message("📐 Mapa centralizado")

    def _redraw_markers(self):
        for mid in list(self.markers):
            try:
                self.canvas.delete(mid)
            except Exception:
                pass
        self.markers.clear()

        # Draw origin marker
        if self.origin:
            x, y = self.origin
            img_w, img_h = self.original_image.size
            disp_w = int(img_w * self.scale)
            disp_h = int(img_h * self.scale)
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            x0 = max((canvas_w - disp_w) // 2, 0) + self.pan_x
            y0 = max((canvas_h - disp_h) // 2, 0) + self.pan_y
            cx = x0 + int(x * self.scale)
            cy = y0 + int(y * self.scale)
            
            # Origin marker with shadow
            r = 10
            shadow = self.canvas.create_oval(cx - r + 2, cy - r + 2, cx + r + 2, cy + r + 2, 
                                           fill='#000000', outline='', tags='marker')
            self.markers.append(shadow)
            
            marker = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, 
                                           fill='#4361ee', outline='white', width=2, tags='marker')
            self.markers.append(marker)
            
            # Inner dot
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, 
                                  fill='white', outline='', tags='marker')
            self.markers.append(marker)
            
            lbl = self.canvas.create_text(cx + 15, cy - 15, text='ORIGEM', 
                                        fill='#4361ee', anchor='nw', 
                                        font=('Arial', 11, 'bold'), tags='marker')
            self.markers.append(lbl)

        # Draw destination markers
        for idx, coord in enumerate(self.destinations):
            if coord:
                x, y = coord
                img_w, img_h = self.original_image.size
                disp_w = int(img_w * self.scale)
                disp_h = int(img_h * self.scale)
                canvas_w = self.canvas.winfo_width()
                canvas_h = self.canvas.winfo_height()
                x0 = max((canvas_w - disp_w) // 2, 0) + self.pan_x
                y0 = max((canvas_h - disp_h) // 2, 0) + self.pan_y
                cx = x0 + int(x * self.scale)
                cy = y0 + int(y * self.scale)
                
                # Destination marker
                r = 8
                shadow = self.canvas.create_oval(cx - r + 2, cy - r + 2, cx + r + 2, cy + r + 2, 
                                               fill='#000000', outline='', tags='marker')
                self.markers.append(shadow)
                
                color = self.route_colors[idx % len(self.route_colors)]
                marker = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, 
                                               fill=color, outline='white', width=2, tags='marker')
                self.markers.append(marker)
                
                marker_text = f'D{idx+1}' if self.multi_destination else 'DESTINO'
                lbl = self.canvas.create_text(cx + 15, cy - 15, text=marker_text, 
                                            fill=color, anchor='nw', 
                                            font=('Arial', 11, 'bold'), tags='marker')
                self.markers.append(lbl)

    def _on_resize(self, event):
        self._update_canvas_image()

    def _update_canvas_image(self):
        canvas_w = max(self.canvas.winfo_width(), 10)
        canvas_h = max(self.canvas.winfo_height(), 10)
        img_w, img_h = self.original_image.size
        ratio = min(canvas_w / img_w, canvas_h / img_h)
        self.scale = ratio
        new_size = (max(1, int(img_w * ratio)), max(1, int(img_h * ratio)))
        resized = self.original_image.resize(new_size, Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        
        self.canvas.delete('all')
        x0 = max((canvas_w - new_size[0]) // 2, 0) + self.pan_x
        y0 = max((canvas_h - new_size[1]) // 2, 0) + self.pan_y
        self.canvas_img_id = self.canvas.create_image(x0, y0, anchor='nw', image=self.tk_image)
        self._redraw_markers()

    def _update_dest_listbox(self):
        if not self.multi_destination:
            return
            
        try:
            self.dest_listbox.delete(0, 'end')
            for idx, (x, y) in enumerate(self.destinations):
                self.dest_listbox.insert('end', f'Destino {idx+1}: {x},{y}')
        except Exception:
            pass

    def _remove_selected_destination(self):
        if not self.multi_destination:
            if self.destinations:
                removed = self.destinations.pop()
                self._log_message(f'🗑️ Destino removido: {removed[0]},{removed[1]}')
                self._redraw_markers()
            return
            
        try:
            sel = self.dest_listbox.curselection()
            if not sel:
                messagebox.showinfo('Seleção', 'Selecione um destino para remover')
                return
            idx = sel[0]
            removed = self.destinations.pop(idx)
            self._update_dest_listbox()
            self._log_message(f'🗑️ Destino {idx+1} removido: {removed[0]},{removed[1]}')
            self._redraw_markers()
        except Exception as e:
            self._log_message(f'❌ Erro ao remover destino: {e}')

    def _on_generate_route(self):
        # Ensure origin is set
        if not self.origin:
            messagebox.showwarning('Origem Ausente', 'Por favor, defina a origem primeiro.')
            return

        # Validate we have destinations
        if not self.destinations:
            messagebox.showwarning('Destinos Ausentes', 'Por favor, defina pelo menos um destino.')
            return

        sx, sy = self.origin
        
        # Clear previous routes
        for tag in self.route_tags:
            try:
                self.canvas.delete(tag)
            except Exception:
                pass
        self.route_tags.clear()

        # Generate routes
        if self.multi_destination:
            self._log_message("🚀 Gerando rotas para múltiplos destinos...")
            for idx, (ex, ey) in enumerate(self.destinations):
                self._log_message(f"📈 Rota {idx+1}: de ({sx},{sy}) para ({ex},{ey})")
                route_txt = self.router.generate_route(sx, sy, ex, ey)
                self._log_message(route_txt)
                tag = f'route_{idx}'
                color = self.route_colors[idx % len(self.route_colors)]
                self._draw_route_from_text(route_txt, color=color, tag=tag)
                self.route_tags.append(tag)
            self._log_message("✅ Todas as rotas geradas com sucesso!")
        else:
            # Single destination
            ex, ey = self.destinations[0]
            self._log_message(f"🚀 Gerando rota: de ({sx},{sy}) para ({ex},{ey})")
            route_txt = self.router.generate_route(sx, sy, ex, ey)
            self._log_message(route_txt)
            self._draw_route_from_text(route_txt, color='#4cc9f0', tag='route_single')
            self.route_tags.append('route_single')
            self._log_message("✅ Rota gerada com sucesso!")

    def _draw_route_from_text(self, txt: str, color='#4cc9f0', tag='route_line'):
        try:
            self.canvas.delete(tag)
        except Exception:
            pass
            
        pts = []
        for line in txt.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                xstr, ystr = line.split(',')
                x = int(float(xstr))
                y = int(float(ystr))
                pts.append((x, y))
            except Exception:
                continue
                
        if len(pts) < 2:
            self._log_message("❌ Rota inválida: pontos insuficientes")
            return
            
        img_w, img_h = self.original_image.size
        disp_w = int(img_w * self.scale)
        disp_h = int(img_h * self.scale)
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        x0 = max((canvas_w - disp_w) // 2, 0) + self.pan_x
        y0 = max((canvas_h - disp_h) // 2, 0) + self.pan_y
        
        coords = []
        for x, y in pts:
            cx = x0 + int(x * self.scale)
            cy = y0 + int(y * self.scale)
            coords.extend([cx, cy])
            
        # Create route line with glow effect
        glow_colors = [('#1a1a1a', 10), ('#000000', 7), (color, 4)]
        for glow_color, width in glow_colors:
            line_id = self.canvas.create_line(*coords, fill=glow_color, width=width, 
                                            tags=(tag,), smooth=True, capstyle='round')
            self.route_tags.append(tag)

    def _clear(self):
        self.origin = None
        self.destinations.clear()
        self.out_text.delete('1.0', 'end')
        self.canvas.delete('all')
        
        if self.multi_destination:
            try:
                self.dest_listbox.delete(0, 'end')
            except Exception:
                pass
                
        # Remove route tags
        for tag in self.route_tags:
            try:
                self.canvas.delete(tag)
            except Exception:
                pass
        self.route_tags.clear()
        
        self._update_canvas_image()
        self._log_message("🗑️ Interface limpa - todos os dados foram resetados")

    def run(self):
        self.root.mainloop()


def main():
    # Start with the start screen
    start_screen = StartScreen()
    start_screen.run()


if __name__ == '__main__':
    main()