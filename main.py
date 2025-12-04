import os
import sys
import ctypes
from ctypes import Structure, POINTER, c_int, c_char_p, byref, create_string_buffer, cdll
import json
from typing import Optional, Tuple, Dict, List

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


# ============================================
# 🆕 ESTRUTURA C: ResultadoRota
# ============================================
class ResultadoRota(Structure):
    _fields_ = [
        ("sequencia_ids", POINTER(c_int)),  # Array de IDs do caminho
        ("num_ids", c_int),                  # Quantidade de IDs
        ("distancia_total", c_int)           # Distância em metros
    ]


def resource_path(filename: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


class RouterLib:
    """Wrapper to load a C library that provides route generation."""

    def __init__(self):
        self.lib = None
        self.pontos_info = {}  # Dicionário: id -> (nome, categoria)
        self._load_lib()
        self._load_pontos_info()

    def _load_lib(self):
        """Carrega DLL e configura TODAS as funções C"""
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
                            ctypes.POINTER(ctypes.c_int),  # id_out
                            ctypes.POINTER(ctypes.c_int),  # x_out
                            ctypes.POINTER(ctypes.c_int)   # y_out
                        ]
                        self.lib.get_ponto_info.restype = ctypes.c_int
                    
                    # ===== NOVAS FUNÇÕES DIJKSTRA =====
                    
                    # Estrutura ResultadoRota
                    class ResultadoRota(ctypes.Structure):
                        _fields_ = [
                            ("sequencia_ids", ctypes.POINTER(ctypes.c_int)),
                            ("num_ids", ctypes.c_int),
                            ("distancia_total", ctypes.c_int)
                        ]
                    
                    self.ResultadoRota = ResultadoRota
                    
                    # calcular_rota(int id_origem, int id_destino)
                    if hasattr(self.lib, 'calcular_rota'):
                        self.lib.calcular_rota.argtypes = [ctypes.c_int, ctypes.c_int]
                        self.lib.calcular_rota.restype = ctypes.POINTER(ResultadoRota)
                    
                    # liberar_resultado(ResultadoRota* resultado)
                    if hasattr(self.lib, 'liberar_resultado'):
                        self.lib.liberar_resultado.argtypes = [ctypes.POINTER(ResultadoRota)]
                        self.lib.liberar_resultado.restype = None
                    
                    # obter_info_vertice(int id, ...)
                    if hasattr(self.lib, 'obter_info_vertice'):
                        self.lib.obter_info_vertice.argtypes = [
                            ctypes.c_int,
                            ctypes.c_char_p, ctypes.c_int,
                            ctypes.c_char_p, ctypes.c_int,
                            ctypes.POINTER(ctypes.c_int),
                            ctypes.POINTER(ctypes.c_int)
                        ]
                        self.lib.obter_info_vertice.restype = ctypes.c_int
                    
                    # obter_numero_total_vertices()
                    if hasattr(self.lib, 'obter_numero_total_vertices'):
                        self.lib.obter_numero_total_vertices.argtypes = []
                        self.lib.obter_numero_total_vertices.restype = ctypes.c_int
                    
                    print("✅ DLL carregada e configurada com sucesso")
                    return
                except Exception as e:
                    print(f"Erro ao carregar DLL: {e}")
                    self.lib = None

    def _load_pontos_info(self):
        """Carrega informações de nome e categoria dos pontos do backend C"""
        if not self.lib or not hasattr(self.lib, 'get_num_pontos') or not hasattr(self.lib, 'get_ponto_info'):
            print("⚠️ Funções de pontos não disponíveis no backend")
            return
        
        try:
            num_pontos = self.lib.get_num_pontos()
            print(f"📋 Carregando {num_pontos} pontos turísticos...")
            
            for i in range(num_pontos):
                nome_buf = ctypes.create_string_buffer(100)
                cat_buf = ctypes.create_string_buffer(50)
                id_val = ctypes.c_int()
                x_val = ctypes.c_int()
                y_val = ctypes.c_int()
                
                result = self.lib.get_ponto_info(
                    i, 
                    nome_buf, 100, 
                    cat_buf, 50, 
                    ctypes.byref(id_val),
                    ctypes.byref(x_val),
                    ctypes.byref(y_val)
                )
                
                if result == 0:
                    nome = nome_buf.value.decode('utf-8', errors='ignore')
                    categoria = cat_buf.value.decode('utf-8', errors='ignore')
                    ponto_id = id_val.value
                    
                    # Apenas pontos turísticos (não esquinas)
                    if categoria != "Esquina" and categoria:
                        self.pontos_info[ponto_id] = (nome, categoria)
        
        except Exception as e:
            print(f"Erro ao carregar pontos turísticos: {e}")
    
    def carregar_lista_pontos(self) -> List[Dict]:
        """
        Carrega TODOS os pontos do BANCO 1 para a lista do frontend.
        Usa coordenadas dos VÉRTICES (calçadas) para Dijkstra.
        """
        if not self.lib:
            print("❌ Biblioteca C não carregada")
            return []
        
        pontos = []
        try:
            # 1. Obter número total de vértices
            if not hasattr(self.lib, 'obter_numero_total_vertices'):
                print("⚠️ Função obter_numero_total_vertices não disponível")
                return []
            
            num_vertices = self.lib.obter_numero_total_vertices()
            print(f"📊 Total de vértices disponíveis: {num_vertices}")
            
            # 2. Para cada vértice, obter informações
            for id_vertice in range(num_vertices):
                # Buffers para informações
                nome_buf = ctypes.create_string_buffer(100)
                categoria_buf = ctypes.create_string_buffer(50)
                x = ctypes.c_int()
                y = ctypes.c_int()
                
                # 3. Chamar função C para obter informações
                resultado = self.lib.obter_info_vertice(
                    id_vertice,
                    nome_buf, 100,        # Nome com limite de 100 chars
                    categoria_buf, 50,    # Categoria com limite de 50 chars
                    ctypes.byref(x),      # Coordenada X (calçada)
                    ctypes.byref(y)       # Coordenada Y (calçada)
                )
                
                # 4. Se sucesso, adicionar à lista
                if resultado == 0:
                    ponto = {
                        'id': id_vertice,
                        'nome': nome_buf.value.decode('utf-8', errors='ignore'),
                        'categoria': categoria_buf.value.decode('utf-8', errors='ignore'),
                        'x_vertice': x.value,    # ✅ Coordenada do VÉRTICE (calçada)
                        'y_vertice': y.value,    # ✅ Para Dijkstra e desenho da rota
                        'x_visual': x.value,     # ⏳ Futuro: coordenada visual (BANCO 2)
                        'y_visual': y.value      # ⏳ Futuro: coordenada visual (BANCO 2)
                    }
                    pontos.append(ponto)
            
            print(f"✅ {len(pontos)} pontos carregados do BANCO 1")
            return pontos
            
        except Exception as e:
            print(f"❌ Erro ao carregar lista de pontos: {e}")
            return []

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

    def calcular_rota_dijkstra(self, id_origem: int, id_destino: int) -> Optional[Dict]:
        """
        Calcula rota usando Dijkstra no backend C.
        Retorna dicionário com sequência de IDs e distância.
        """
        if not self.lib:
            print("❌ Biblioteca C não carregada")
            return None
        
        # ⚠️ VALIDAÇÃO: origem != destino
        if id_origem == id_destino:
            print("❌ Origem e destino são iguais")
            return None
        
        try:
            print(f"🔄 Calculando rota Dijkstra: {id_origem} → {id_destino}")
            
            # 1. CHAMAR FUNÇÃO C PRINCIPAL
            resultado_ptr = self.lib.calcular_rota(id_origem, id_destino)
            
            # 2. VERIFICAR SE FOI POSSÍVEL CALCULAR
            if not resultado_ptr:
                print("❌ Não foi possível calcular a rota (retornou NULL)")
                return None
            
            # 3. EXTRAIR RESULTADO
            resultado = resultado_ptr.contents
            
            # 4. CONVERTER PARA DICIONÁRIO PYTHON
            rota_dict = {
                'sequencia_ids': [],
                'num_ids': resultado.num_ids,
                'distancia_total': resultado.distancia_total
            }
            
            # 5. EXTRAIR SEQUÊNCIA DE IDs
            for i in range(resultado.num_ids):
                rota_dict['sequencia_ids'].append(resultado.sequencia_ids[i])
            
            print(f"✅ Rota calculada: {rota_dict['num_ids']} pontos, "
                  f"{rota_dict['distancia_total']} metros")
            
            # 6. LIBERAR MEMÓRIA C
            self.lib.liberar_resultado(resultado_ptr)
            
            return rota_dict
            
        except Exception as e:
            print(f"❌ Erro ao calcular rota: {e}")
            import traceback
            traceback.print_exc()
            return None

    def obter_coordenadas_por_id(self, ponto_id: int) -> Optional[Tuple[int, int]]:
        """
        Obtém coordenadas (x, y) de um ponto pelo ID usando backend C.
        (Compatibilidade com código antigo)
        """
        return self.obter_coordenadas_vertice(ponto_id)
    
    def obter_coordenadas_vertice(self, id_vertice: int) -> Optional[Tuple[int, int]]:
        """
        Obtém coordenadas do VÉRTICE (calçada) para um ID específico.
        Usado para desenhar a rota no mapa.
        """
        if not self.lib:
            return None
        
        try:
            x = ctypes.c_int()
            y = ctypes.c_int()
            
            # ⚠️ IMPORTANTE: Usa obter_info_vertice que retorna coordenadas do VÉRTICE
            resultado = self.lib.obter_info_vertice(
                id_vertice,
                None, 0,   # Não precisa do nome
                None, 0,   # Não precisa da categoria
                ctypes.byref(x),  # Coordenada X do vértice
                ctypes.byref(y)   # Coordenada Y do vértice
            )
            
            if resultado == 0:
                return (x.value, y.value)
            else:
                print(f"⚠️ Vértice {id_vertice} não encontrado")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao obter coordenadas: {e}")
            return None


class ModernMapApp:
    """Aplicação de navegação com origem -> destino único"""
    
    # Mapeamento de categorias para ícones
    CATEGORIA_ICONE = {
        "Adega": "Adega.png",
        "Banco": "Banco.png",
        "Bar": "Bar.png",
        "Barbearia": "Barbearia.png",
        "Cafeteria": "Cafeteria.png",
        "Centro Histórico": "Centro Histórico.png",
        "Cervejaria": "Cervejaria.png",
        "Comércio": "Comércio.png",
        "Entretenimento": "Entretenimento.png",
        "Estacionamento": "Estacionamento.png",
        "Galeria": "Galeria.png",
        "Hotel": "Hotel.png",
        "Moda e Vestuário": "Moda e Vestuário.png",
        "Padaria": "Padaria.png",
        "Papelaria": "Papelaria.png",
        "Posto de gasolina": "Posto de gasolina.png",
        "Restaurante": "Restaurante.png",
        "Saúde": "Saude.png",
        "Supermercado": "Super Mercado.png",
        "Doces": "Restaurante.png",  # Fallback
    }
    
    def __init__(self):
        self.image_path = resource_path('perimetro-mapa.png')
        
        if not os.path.exists(self.image_path):
            messagebox.showerror('Erro', f'Arquivo não encontrado: {self.image_path}')
            raise SystemExit(1)

        if Image is None or ImageTk is None:
            messagebox.showerror('Dependência ausente', 'Pillow não está instalado. Instale com: pip install pillow')
            raise SystemExit(1)

        # Carregar imagem do mapa
        self.original_image = Image.open(self.image_path)

        # Router library wrapper
        self.router = RouterLib()

        # Carregar pins.json
        self.pins = self._load_pins()
        
        # Carregar ícones
        self.icones = self._load_icons()

        # UI com tema moderno
        if ctk:
            ctk.set_appearance_mode('Dark')
            ctk.set_default_color_theme('blue')
            self.root = ctk.CTk()
            self.is_ctk = True
        else:
            self.root = tk.Tk()
            self.is_ctk = False

        self.root.title("Sistema de Navegação - Origem → Destino")
        self.root.geometry('1400x900')
        self.root.minsize(1200, 700)

        # Configure grid para layout responsivo
        self.root.grid_columnconfigure(0, weight=0)  # Painel de controles
        self.root.grid_columnconfigure(1, weight=1)  # Área do mapa
        self.root.grid_rowconfigure(0, weight=1)

        # Estado
        self.scale = 1.0
        self.canvas_img_id = None
        self.tk_image = None
        self.origin_id: Optional[int] = None  # ID do ponto de origem
        self.destination_id: Optional[int] = None  # ID do ponto de destino
        self.markers: List[int] = []
        self.icon_markers: Dict[int, int] = {}  # id -> canvas_id
        self.pan_x = 0
        self.pan_y = 0
        self._drag_start = None
        self._search_debounce_id = None  # Para debounce da busca
        self._lazy_load_id = None  # Para lazy loading da lista
        self._all_pontos = []  # Cache de todos os pontos
        self._loaded_count = 0  # Contador de itens carregados
        self.BATCH_SIZE = 20  # Carregar 20 itens por vez
        self.route_active = False  # Flag para indicar se há uma rota ativa
        self.route_lines: List[int] = []

        # Build UI
        self._build_ui()

        # Renderização inicial
        self.root.after(100, self._update_canvas_image)
        self.root.after(200, self._draw_all_icons)

    def _load_pins(self) -> Dict:
        """Carrega o arquivo pins.json"""
        pins_path = resource_path('pins.json')
        try:
            with open(pins_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Converter para dict com id como chave
                pins_dict = {}
                for pin in data['pins']:
                    pins_dict[pin['id']] = (pin['x'], pin['y'])
                return pins_dict
        except Exception as e:
            print(f"Erro ao carregar pins.json: {e}")
            messagebox.showerror("Erro", f"Não foi possível carregar pins.json: {e}")
            return {}

    def _load_icons(self) -> Dict:
        """Carrega todos os ícones da pasta assets"""
        icons = {}
        assets_path = resource_path('assets')
        
        if not os.path.exists(assets_path):
            print(f"Pasta assets não encontrada: {assets_path}")
            return icons
        
        for filename, icon_file in self.CATEGORIA_ICONE.items():
            icon_path = os.path.join(assets_path, icon_file)
            if os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path)
                    # Redimensionar para tamanho padrão
                    img = img.resize((32, 32), Image.Resampling.LANCZOS)
                    icons[filename] = img
                except Exception as e:
                    print(f"Erro ao carregar ícone {icon_file}: {e}")
        
        return icons

    def _build_ui(self):
        # Painel esquerdo - Controles
        if self.is_ctk:
            self.control_frame = ctk.CTkFrame(self.root, width=380, corner_radius=15)
        else:
            self.control_frame = tk.Frame(self.root, width=380, bg='#2b2b2b')
        
        self.control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.control_frame.grid_propagate(False)

        # Painel direito - Mapa
        if self.is_ctk:
            self.map_frame = ctk.CTkFrame(self.root, corner_radius=15)
        else:
            self.map_frame = tk.Frame(self.root, bg='#2b2b2b')
        
        self.map_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Configurar grid do mapa
        self.map_frame.grid_columnconfigure(0, weight=1)
        self.map_frame.grid_rowconfigure(0, weight=1)

        # Criar canvas no mapa
        self.canvas = tk.Canvas(self.map_frame, bg='#1a1a1a', highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Build painel de controle
        self._build_control_panel()

        # Bind eventos
        self.canvas.bind('<Button-1>', self._on_canvas_click)
        self.canvas.bind('<ButtonPress-1>', self._on_left_press)
        self.canvas.bind('<B1-Motion>', self._on_left_drag)
        self.root.bind('<Configure>', self._on_resize)

    def _build_control_panel(self):
        # Header
        header_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        header_frame.pack(fill='x', padx=15, pady=15)
        
        # Título
        if self.is_ctk:
            title = ctk.CTkLabel(header_frame, text="🗺️ Sistema de Navegação", 
                               font=('Arial', 18, 'bold'), text_color="#4cc9f0")
            title.pack(anchor='center')
            
            subtitle = ctk.CTkLabel(header_frame, text="Origem → Destino", 
                                   font=('Arial', 12), text_color="#888888")
            subtitle.pack(anchor='center', pady=(5, 0))
        else:
            title = tk.Label(header_frame, text="🗺️ Sistema de Navegação", 
                           font=('Arial', 16, 'bold'), bg='#2b2b2b', fg='#4cc9f0')
            title.pack(anchor='center')
            
            subtitle = tk.Label(header_frame, text="Origem → Destino", 
                              font=('Arial', 11), bg='#2b2b2b', fg='#888888')
            subtitle.pack(anchor='center', pady=(5, 0))

        self._create_separator()

        # Seleção Atual
        if self.is_ctk:
            selection_label = ctk.CTkLabel(self.control_frame, text="SELEÇÃO ATUAL", 
                                         font=('Arial', 12, 'bold'), text_color="#4cc9f0")
            selection_label.pack(pady=(10, 5))
        else:
            selection_label = tk.Label(self.control_frame, text="SELEÇÃO ATUAL", 
                                     font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='#4cc9f0')
            selection_label.pack(pady=(10, 5))

        # Frame de seleção
        selection_frame = ctk.CTkFrame(self.control_frame) if self.is_ctk else tk.Frame(self.control_frame, bg='#1a1a1a')
        selection_frame.pack(fill='x', padx=15, pady=5)

        if self.is_ctk:
            self.origin_label = ctk.CTkLabel(selection_frame, text="📍 Origem: Não selecionada", 
                                           font=('Arial', 11), text_color="#ffffff", anchor='w')
            self.origin_label.pack(fill='x', padx=10, pady=5)
            
            self.dest_label = ctk.CTkLabel(selection_frame, text="🎯 Destino: Não selecionado", 
                                         font=('Arial', 11), text_color="#ffffff", anchor='w')
            self.dest_label.pack(fill='x', padx=10, pady=5)
        else:
            self.origin_label = tk.Label(selection_frame, text="📍 Origem: Não selecionada", 
                                        font=('Arial', 10), bg='#1a1a1a', fg='#ffffff', anchor='w')
            self.origin_label.pack(fill='x', padx=10, pady=5)
            
            self.dest_label = tk.Label(selection_frame, text="🎯 Destino: Não selecionado", 
                                      font=('Arial', 10), bg='#1a1a1a', fg='#ffffff', anchor='w')
            self.dest_label.pack(fill='x', padx=10, pady=5)

        self._create_separator()

        # Botões de ação
        if self.is_ctk:
            action_label = ctk.CTkLabel(self.control_frame, text="AÇÕES", 
                                      font=('Arial', 12, 'bold'), text_color="#4cc9f0")
            action_label.pack(pady=(10, 5))
        else:
            action_label = tk.Label(self.control_frame, text="AÇÕES", 
                                  font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='#4cc9f0')
            action_label.pack(pady=(10, 5))

        btn_container = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        btn_container.pack(fill='x', padx=15, pady=10)

        buttons = [
            ("🚀 Calcular Rota", self._generate_route, "#4cc9f0"),
            ("🗑️ Limpar Tudo", self._clear, "#ef476f"),
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

        # Lista de pontos turísticos
        if self.is_ctk:
            spots_label = ctk.CTkLabel(self.control_frame, text="PONTOS TURÍSTICOS", 
                                     font=('Arial', 12, 'bold'), text_color="#4cc9f0")
            spots_label.pack(pady=(10, 5))
        else:
            spots_label = tk.Label(self.control_frame, text="PONTOS TURÍSTICOS", 
                                 font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='#4cc9f0')
            spots_label.pack(pady=(10, 5))

        # Campo de busca
        search_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        search_frame.pack(fill='x', padx=15, pady=(0, 5))

        if self.is_ctk:
            self.search_var = tk.StringVar()
            self.search_var.trace('w', lambda *args: self._on_search_change())
            self.search_entry = ctk.CTkEntry(search_frame, 
                                            placeholder_text="🔍 Buscar por nome...",
                                            textvariable=self.search_var,
                                            font=('Arial', 11),
                                            height=35)
            self.search_entry.pack(fill='x')
        else:
            self.search_var = tk.StringVar()
            self.search_var.trace('w', lambda *args: self._on_search_change())
            self.search_entry = tk.Entry(search_frame, 
                                        textvariable=self.search_var,
                                        bg='#3b3b3b', fg='white', 
                                        font=('Arial', 10),
                                        insertbackground='white')
            self.search_entry.pack(fill='x')
            # Placeholder para tk
            self.search_entry.insert(0, "🔍 Buscar por nome...")
            self.search_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(e))
            self.search_entry.bind('<FocusOut>', lambda e: self._restore_placeholder(e))

        # Frame com scroll para lista de pontos
        list_container = ctk.CTkFrame(self.control_frame) if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        list_container.pack(fill='both', expand=True, padx=15, pady=5)

        if self.is_ctk:
            scroll_frame = ctk.CTkScrollableFrame(list_container)
            scroll_frame.pack(fill='both', expand=True)
            self.spots_container = scroll_frame
        else:
            canvas_scroll = tk.Canvas(list_container, bg='#2b2b2b', highlightthickness=0)
            scrollbar = tk.Scrollbar(list_container, orient='vertical', command=canvas_scroll.yview)
            scroll_frame = tk.Frame(canvas_scroll, bg='#2b2b2b')
            
            scroll_frame.bind('<Configure>', lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all')))
            canvas_scroll.create_window((0, 0), window=scroll_frame, anchor='nw')
            canvas_scroll.configure(yscrollcommand=scrollbar.set)
            
            canvas_scroll.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            self.spots_container = scroll_frame

        # Adicionar botões de pontos turísticos
        self._populate_tourist_spots()

        self._create_separator()

        # Controles de zoom
        if self.is_ctk:
            zoom_label = ctk.CTkLabel(self.control_frame, text="CONTROLES DO MAPA", 
                                    font=('Arial', 12, 'bold'), text_color="#4cc9f0")
            zoom_label.pack(pady=(10, 5))
        else:
            zoom_label = tk.Label(self.control_frame, text="CONTROLES DO MAPA", 
                                font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='#4cc9f0')
            zoom_label.pack(pady=(10, 5))

        zoom_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent") if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        zoom_frame.pack(fill='x', padx=15, pady=10)

        if self.is_ctk:
            ctk.CTkButton(zoom_frame, text="➕ Zoom In", command=self._zoom_in,
                        fg_color="#4361ee", font=('Arial', 11), height=35).pack(side='left', fill='x', expand=True, padx=2)
            ctk.CTkButton(zoom_frame, text="➖ Zoom Out", command=self._zoom_out,
                        fg_color="#f72585", font=('Arial', 11), height=35).pack(side='left', fill='x', expand=True, padx=2)
            ctk.CTkButton(zoom_frame, text="📐 Reset", command=self._reset_view,
                        fg_color="#4cc9f0", font=('Arial', 11), height=35).pack(side='left', fill='x', expand=True, padx=2)
        else:
            tk.Button(zoom_frame, text="➕", command=self._zoom_in, 
                    bg="#4361ee", fg='white', font=('Arial', 10), height=2,
                    relief='flat', width=5).pack(side='left', fill='x', expand=True, padx=2)
            tk.Button(zoom_frame, text="➖", command=self._zoom_out, 
                    bg="#f72585", fg='white', font=('Arial', 10), height=2,
                    relief='flat', width=5).pack(side='left', fill='x', expand=True, padx=2)
            tk.Button(zoom_frame, text="📐", command=self._reset_view, 
                    bg="#4cc9f0", fg='white', font=('Arial', 10), height=2,
                    relief='flat', width=5).pack(side='left', fill='x', expand=True, padx=2)

        self._create_separator()

        # Log/Output
        if self.is_ctk:
            log_label = ctk.CTkLabel(self.control_frame, text="LOG", 
                                   font=('Arial', 12, 'bold'), text_color="#4cc9f0")
            log_label.pack(pady=(10, 5))
        else:
            log_label = tk.Label(self.control_frame, text="LOG", 
                               font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='#4cc9f0')
            log_label.pack(pady=(10, 5))

        text_frame = ctk.CTkFrame(self.control_frame) if self.is_ctk else tk.Frame(self.control_frame, bg='#2b2b2b')
        text_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))

        if self.is_ctk:
            self.out_text = ctk.CTkTextbox(text_frame, font=('Consolas', 10), 
                                         fg_color='#1a1a1a', text_color='#00ff88',
                                         height=100)
            self.out_text.pack(fill='both', expand=True, padx=5, pady=5)
        else:
            self.out_text = tk.Text(text_frame, font=('Consolas', 9), 
                                  bg='#1a1a1a', fg='#00ff88',
                                  insertbackground='white', wrap='word',
                                  relief='flat', height=6)
            scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.out_text.yview)
            self.out_text.configure(yscrollcommand=scrollbar.set)
            
            self.out_text.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')

        self._log_message("✅ Aplicação iniciada. Clique em um ícone para selecionar origem/destino.")

    def _populate_tourist_spots(self):
        """Popula a lista de pontos turísticos com botões - com lazy loading"""
        # Cancelar lazy loading pendente
        if self._lazy_load_id:
            self.root.after_cancel(self._lazy_load_id)
            self._lazy_load_id = None
        
        # Limpar botões existentes
        for widget in self.spots_container.winfo_children():
            widget.destroy()
        
        # Obter texto de busca
        search_text = self.search_var.get().strip().lower() if hasattr(self, 'search_var') else ""
        
        # Ignorar placeholder do tkinter
        if search_text == "🔍 buscar por nome...":
            search_text = ""
        
        # Filtrar pontos
        filtered_pontos = []
        for ponto_id in sorted(self.pins.keys()):
            if ponto_id in self.router.pontos_info:
                nome, categoria = self.router.pontos_info[ponto_id]
                
                # Filtrar por busca - se search_text está vazio, mostra todos
                if search_text and search_text not in nome.lower():
                    continue
                
                filtered_pontos.append((ponto_id, nome, categoria))
        
        # Guardar lista filtrada e resetar contador
        self._all_pontos = filtered_pontos
        self._loaded_count = 0
        
        # Se tem resultados, carregar primeiro lote
        if filtered_pontos:
            self._load_next_batch()
        # Se buscou algo mas não encontrou
        elif search_text:
            if self.is_ctk:
                no_results = ctk.CTkLabel(self.spots_container, 
                                         text="Nenhum resultado encontrado",
                                         font=('Arial', 10),
                                         text_color='#888888')
                no_results.pack(pady=10)
            else:
                no_results = tk.Label(self.spots_container, 
                                     text="Nenhum resultado encontrado",
                                     font=('Arial', 10),
                                     bg='#2b2b2b', fg='#888888')
                no_results.pack(pady=10)

    def _load_next_batch(self):
        """Carrega próximo lote de itens"""
        start_idx = self._loaded_count
        end_idx = min(start_idx + self.BATCH_SIZE, len(self._all_pontos))
        
        # Carregar lote atual
        for i in range(start_idx, end_idx):
            ponto_id, nome, categoria = self._all_pontos[i]
            
            # Criar botão para este ponto
            if self.is_ctk:
                btn = ctk.CTkButton(self.spots_container, 
                                  text=f"{ponto_id}: {nome}",
                                  command=lambda pid=ponto_id: self._select_point_from_list(pid),
                                  fg_color='#3b3b3b',
                                  hover_color='#4a4a4a',
                                  text_color='#ffffff',
                                  font=('Arial', 10),
                                  height=30,
                                  anchor='w',
                                  corner_radius=6)
                btn.pack(fill='x', pady=2)
            else:
                btn = tk.Button(self.spots_container, 
                              text=f"{ponto_id}: {nome}",
                              command=lambda pid=ponto_id: self._select_point_from_list(pid),
                              bg='#3b3b3b', fg='white', font=('Arial', 9),
                              relief='flat', height=1, anchor='w', bd=0)
                btn.pack(fill='x', pady=2, padx=2)
        
        self._loaded_count = end_idx
        
        # Se ainda tem mais itens, agendar próximo lote
        if self._loaded_count < len(self._all_pontos):
            self._lazy_load_id = self.root.after(50, self._load_next_batch)

    def _filter_tourist_spots(self):
        """Filtra a lista de pontos turísticos baseado no texto de busca"""
        self._populate_tourist_spots()

    def _on_search_change(self):
        """Callback quando o texto de busca muda - com debounce"""
        # Cancelar timer anterior se existir
        if self._search_debounce_id:
            self.root.after_cancel(self._search_debounce_id)
        
        # Mostrar indicador de carregamento (opcional)
        # Agendar nova busca após 400ms (aumentado de 300ms)
        self._search_debounce_id = self.root.after(400, self._filter_tourist_spots)

    def _clear_placeholder(self, event):
        """Remove o placeholder quando o campo ganha foco"""
        if not self.is_ctk and self.search_entry.get() == "🔍 Buscar por nome...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='white')

    def _restore_placeholder(self, event):
        """Restaura o placeholder quando o campo perde foco"""
        if not self.is_ctk and self.search_entry.get() == "":
            self.search_entry.insert(0, "🔍 Buscar por nome...")
            self.search_entry.config(fg='#888888')

    def _select_point_from_list(self, ponto_id: int):
        """Seleciona um ponto da lista para origem ou destino"""
        nome, _ = self.router.pontos_info.get(ponto_id, ("Desconhecido", ""))
        
        # Perguntar se é origem ou destino
        response = messagebox.askquestion("Selecionar Ponto", 
                                         f"Definir '{nome}' como:\n\nSim = Origem\nNão = Destino",
                                         icon='question')
        
        if response == 'yes':
            self.origin_id = ponto_id
            self.origin_label.configure(text=f"📍 Origem: {nome}")
            self._log_message(f"📍 Origem: {nome} (ID: {ponto_id})")
        else:
            self.destination_id = ponto_id
            self.dest_label.configure(text=f"🎯 Destino: {nome}")
            self._log_message(f"🎯 Destino: {nome} (ID: {ponto_id})")
        
        self._redraw_markers()

    def _draw_all_icons(self):
        """Desenha todos os ícones dos pontos turísticos no mapa"""
        # Limpar ícones existentes
        for canvas_id in self.icon_markers.values():
            try:
                self.canvas.delete(canvas_id)
            except:
                pass
        self.icon_markers.clear()

        # Se há rota ativa, mostrar apenas origem e destino
        if self.route_active and self.origin_id and self.destination_id:
            # Desenhar apenas origem
            if self.origin_id in self.pins:
                x, y = self.pins[self.origin_id]
                nome, categoria = self.router.pontos_info.get(self.origin_id, ("Origem", "Comércio"))
                self._draw_icon(self.origin_id, x, y, categoria)
            
            # Desenhar apenas destino
            if self.destination_id in self.pins:
                x, y = self.pins[self.destination_id]
                nome, categoria = self.router.pontos_info.get(self.destination_id, ("Destino", "Comércio"))
                self._draw_icon(self.destination_id, x, y, categoria)
        else:
            # Desenhar todos os ícones
            for ponto_id, (x, y) in self.pins.items():
                if ponto_id in self.router.pontos_info:
                    nome, categoria = self.router.pontos_info[ponto_id]
                    self._draw_icon(ponto_id, x, y, categoria)

    def _draw_icon(self, ponto_id: int, x: int, y: int, categoria: str):
        """Desenha um ícone no mapa"""
        # Obter imagem do ícone
        icon_img = self.icones.get(categoria)
        if not icon_img:
            # Fallback para ícone genérico
            icon_img = self.icones.get("Comércio")
        
        if not icon_img:
            return  # Sem ícone disponível

        # Converter coordenadas da imagem para canvas
        canvas_x, canvas_y = self._img_to_canvas(x, y)
        if canvas_x is None:
            return

        # Redimensionar ícone baseado no zoom
        icon_size = int(32 * min(self.scale, 1.5))
        icon_resized = icon_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        
        # Converter para PhotoImage
        photo = ImageTk.PhotoImage(icon_resized)
        
        # Desenhar no canvas com anchor='s' para posicionar a ponta do pin na coordenada
        canvas_id = self.canvas.create_image(canvas_x, canvas_y, image=photo, 
                                            anchor='s', tags=f"icon_{ponto_id}")
        
        # Guardar referência para evitar garbage collection
        if not hasattr(self, '_icon_photos'):
            self._icon_photos = {}
        self._icon_photos[ponto_id] = photo
        
        # Guardar canvas_id
        self.icon_markers[ponto_id] = canvas_id
        
        # Bind click event
        self.canvas.tag_bind(f"icon_{ponto_id}", '<Button-1>', 
                            lambda e, pid=ponto_id: self._on_icon_click(pid))

    def _on_icon_click(self, ponto_id: int):
        """Handler para clique em ícone"""
        nome, _ = self.router.pontos_info.get(ponto_id, ("Desconhecido", ""))
        
        # Se não há origem, definir como origem
        if self.origin_id is None:
            self.origin_id = ponto_id
            self.origin_label.configure(text=f"📍 Origem: {nome}")
            self._log_message(f"📍 Origem: {nome} (ID: {ponto_id})")
        # Se há origem mas não destino, definir como destino
        elif self.destination_id is None:
            # ⚠️ VALIDAÇÃO: destino != origem
            if ponto_id == self.origin_id:
                messagebox.showwarning("Aviso", "Destino não pode ser igual à origem!")
                return
            self.destination_id = ponto_id
            self.dest_label.configure(text=f"🎯 Destino: {nome}")
            self._log_message(f"🎯 Destino: {nome} (ID: {ponto_id})")
        # Se ambos já estão definidos, perguntar o que fazer
        else:
            response = messagebox.askquestion("Substituir?", 
                                             f"Substituir origem ou destino com '{nome}'?\n\nSim = Origem\nNão = Destino",
                                             icon='question')
            if response == 'yes':
                # ⚠️ VALIDAÇÃO: novo origem != destino atual
                if ponto_id == self.destination_id:
                    messagebox.showwarning("Aviso", "Origem não pode ser igual ao destino!")
                    return
                self.origin_id = ponto_id
                self.origin_label.configure(text=f"📍 Origem: {nome}")
                self._log_message(f"📍 Origem atualizada: {nome} (ID: {ponto_id})")
            else:
                # ⚠️ VALIDAÇÃO: novo destino != origem atual
                if ponto_id == self.origin_id:
                    messagebox.showwarning("Aviso", "Destino não pode ser igual à origem!")
                    return
                self.destination_id = ponto_id
                self.dest_label.configure(text=f"🎯 Destino: {nome}")
                self._log_message(f"🎯 Destino atualizado: {nome} (ID: {ponto_id})")
        
        self._redraw_markers()

    def _img_to_canvas(self, ix: int, iy: int) -> Tuple[Optional[int], Optional[int]]:
        """Converte coordenadas da imagem para coordenadas do canvas"""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_w, img_h = self.original_image.size
        
        scale = self.scale
        disp_w = int(img_w * scale)
        disp_h = int(img_h * scale)
        x0 = max((canvas_w - disp_w) // 2, 0) + self.pan_x
        y0 = max((canvas_h - disp_h) // 2, 0) + self.pan_y
        
        cx = int(ix * scale) + x0
        cy = int(iy * scale) + y0
        
        return (cx, cy)

    def _canvas_to_img(self, cx: int, cy: int) -> Tuple[Optional[int], Optional[int]]:
        """Converte coordenadas do canvas para coordenadas da imagem"""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_w, img_h = self.original_image.size
        
        scale = self.scale
        disp_w = int(img_w * scale)
        disp_h = int(img_h * scale)
        x0 = max((canvas_w - disp_w) // 2, 0) + self.pan_x
        y0 = max((canvas_h - disp_h) // 2, 0) + self.pan_y
        
        ix = int((cx - x0) / scale)
        iy = int((cy - y0) / scale)
        
        if ix < 0 or iy < 0 or ix >= img_w or iy >= img_h:
            return (None, None)
        
        return (ix, iy)

    def _generate_route(self):
        """Gera rota entre origem e destino usando Dijkstra"""
        # ⚠️ VALIDAÇÃO FINAL
        if self.origin_id is None:
            messagebox.showwarning("Origem não definida", "Por favor, selecione um ponto de origem.")
            return
        
        if self.destination_id is None:
            messagebox.showwarning("Destino não definido", "Por favor, selecione um ponto de destino.")
            return
        
        if self.origin_id == self.destination_id:
            messagebox.showwarning("Pontos iguais", "Origem e destino não podem ser o mesmo ponto.")
            return

        self._log_message(f"🚀 Calculando rota de ID {self.origin_id} para ID {self.destination_id}...")
        
        try:
            # ===== USAR DIJKSTRA DO BACKEND C =====
            resultado = self.router.calcular_rota_dijkstra(self.origin_id, self.destination_id)
            
            if resultado is None:
                self._log_message("❌ Erro ao calcular rota com Dijkstra")
                messagebox.showerror("Erro", "Não foi possível calcular a rota")
                return
            
            # Extrair dados do resultado
            sequencia_ids = resultado['sequencia_ids']
            distancia_total = resultado['distancia_total']
            num_pontos = resultado['num_ids']
            
            if len(sequencia_ids) < 2:
                self._log_message("❌ Rota inválida (menos de 2 pontos)")
                messagebox.showerror("Erro", "Rota calculada é inválida")
                return
            
            self._log_message(f"✅ Rota encontrada com {num_pontos} vértices")
            self._log_message(f"📏 Distância total: {distancia_total} metros")
            self._log_message(f"🛤️  Caminho: {' → '.join(map(str, sequencia_ids))}")
            
            # Converter IDs para coordenadas (do backend C - coordenadas do grafo)
            points = []
            for ponto_id in sequencia_ids:
                coords = self.router.obter_coordenadas_vertice(ponto_id)
                if coords:
                    points.append(coords)
                else:
                    self._log_message(f"⚠️ Vértice {ponto_id} não encontrado (pulando)")
            
            if len(points) < 2:
                self._log_message("❌ Coordenadas insuficientes para desenhar rota")
                messagebox.showerror("Erro", "Não foi possível obter coordenadas da rota")
                return
            
            # Desenhar rota
            self._draw_route(points)
            
            # Marcar rota como ativa e redesenhar ícones (mostrando apenas origem/destino)
            self.route_active = True
            self._draw_all_icons()
            
            self._log_message(f"✅ Rota desenhada com sucesso!")
            
        except Exception as e:
            self._log_message(f"❌ Erro ao processar rota: {e}")
            messagebox.showerror("Erro", f"Erro ao processar rota: {e}")


    def _draw_route(self, points: List[Tuple[int, int]]):
        """Desenha a rota no mapa"""
        # Limpar rotas anteriores
        for line_id in self.route_lines:
            try:
                self.canvas.delete(line_id)
            except:
                pass
        self.route_lines.clear()

        # Desenhar linhas conectando os pontos
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            cx1, cy1 = self._img_to_canvas(x1, y1)
            cx2, cy2 = self._img_to_canvas(x2, y2)
            
            if cx1 is not None and cx2 is not None:
                line_id = self.canvas.create_line(cx1, cy1, cx2, cy2, 
                                                  fill='#4cc9f0', width=3,
                                                  tags='route')
                self.route_lines.append(line_id)

    def _redraw_markers(self):
        """Redesenha marcadores de origem e destino"""
        # Limpar marcadores anteriores
        for mid in self.markers:
            try:
                self.canvas.delete(mid)
            except:
                pass
        self.markers.clear()

        # Desenhar origem
        if self.origin_id and self.origin_id in self.pins:
            x, y = self.pins[self.origin_id]
            cx, cy = self._img_to_canvas(x, y)
            if cx is not None:
                # Círculo verde para origem
                r = 8
                marker = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                                fill='#00ff00', outline='#ffffff',
                                                width=2, tags='marker_origin')
                self.markers.append(marker)

        # Desenhar destino
        if self.destination_id and self.destination_id in self.pins:
            x, y = self.pins[self.destination_id]
            cx, cy = self._img_to_canvas(x, y)
            if cx is not None:
                # Círculo vermelho para destino
                r = 8
                marker = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                                fill='#ff0000', outline='#ffffff',
                                                width=2, tags='marker_dest')
                self.markers.append(marker)

    def _clear(self):
        """Limpa todas as seleções e rotas"""
        self.origin_id = None
        self.destination_id = None
        self.origin_label.configure(text="📍 Origem: Não selecionada")
        self.dest_label.configure(text="🎯 Destino: Não selecionado")
        
        # Marcar rota como inativa
        self.route_active = False
        
        # Limpar rotas
        for line_id in self.route_lines:
            try:
                self.canvas.delete(line_id)
            except:
                pass
        self.route_lines.clear()
        
        # Limpar marcadores
        for mid in self.markers:
            try:
                self.canvas.delete(mid)
            except:
                pass
        self.markers.clear()
        
        # Redesenhar todos os ícones
        self._draw_all_icons()
        
        self._log_message("🗑️ Tudo limpo. Selecione novos pontos.")

    def _update_canvas_image(self):
        """Atualiza a imagem do mapa no canvas"""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w <= 1 or canvas_h <= 1:
            return

        img_w, img_h = self.original_image.size
        scale = self.scale
        disp_w = int(img_w * scale)
        disp_h = int(img_h * scale)

        resized = self.original_image.resize((disp_w, disp_h), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)

        x0 = max((canvas_w - disp_w) // 2, 0) + self.pan_x
        y0 = max((canvas_h - disp_h) // 2, 0) + self.pan_y

        if self.canvas_img_id:
            self.canvas.delete(self.canvas_img_id)
        
        self.canvas_img_id = self.canvas.create_image(x0, y0, anchor='nw', image=self.tk_image, tags='map_image')
        self.canvas.tag_lower('map_image')
        
        # Redesenhar ícones
        self._draw_all_icons()
        
        # Redesenhar marcadores
        self._redraw_markers()

    def _on_resize(self, event):
        """Handler para resize da janela"""
        self._update_canvas_image()

    def _on_canvas_click(self, event):
        """Handler para cliques no canvas (fora dos ícones)"""
        # Este método já não é necessário para seleção, mas mantemos para debug
        ix, iy = self._canvas_to_img(event.x, event.y)
        if ix is not None:
            self._log_message(f"📌 Clique em: ({ix}, {iy})")

    def _on_left_press(self, event):
        """Handler para pressionar botão esquerdo"""
        if (event.state & 0x4) != 0:  # Ctrl pressionado
            self._drag_start = (event.x, event.y, self.pan_x, self.pan_y)

    def _on_left_drag(self, event):
        """Handler para arrastar com botão esquerdo"""
        if not self._drag_start:
            return
        sx, sy, px, py = self._drag_start
        dx = event.x - sx
        dy = event.y - sy
        self.pan_x = px + dx
        self.pan_y = py + dy
        self._update_canvas_image()

    def _zoom_in(self):
        """Aumenta o zoom"""
        self.scale = min(self.scale * 1.2, 5.0)
        self._update_canvas_image()
        self._log_message("🔍 Zoom aumentado")

    def _zoom_out(self):
        """Diminui o zoom"""
        self.scale = max(self.scale / 1.2, 0.1)
        self._update_canvas_image()
        self._log_message("🔍 Zoom reduzido")

    def _reset_view(self):
        """Reseta zoom e pan"""
        self.scale = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self._update_canvas_image()
        self._log_message("📐 Visualização resetada")

    def _create_separator(self):
        """Cria um separador visual"""
        if self.is_ctk:
            separator = ctk.CTkFrame(self.control_frame, height=2, fg_color="#3b3b3b")
            separator.pack(fill='x', padx=20, pady=10)
        else:
            separator = tk.Frame(self.control_frame, height=2, bg="#3b3b3b")
            separator.pack(fill='x', padx=20, pady=10)

    def _darken_color(self, color, factor=0.8):
        """Escurece uma cor hex para efeito hover"""
        if color.startswith('#'):
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            darkened = tuple(max(0, int(c * factor)) for c in rgb)
            return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
        return color

    def _log_message(self, message: str):
        """Adiciona mensagem ao log"""
        self.out_text.insert('end', f"{message}\n")
        self.out_text.see('end')

    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()


def main():
    """Função principal"""
    app = ModernMapApp()
    app.run()


if __name__ == '__main__':
    main()
