#!/usr/bin/env python3
import json
import os
import sys
import subprocess
import time

# Configuration
CONFIG_DIR = os.path.expanduser("~/.WorkspaceManager")
DATA_FILE = os.path.join(CONFIG_DIR, "projects.json")

# Colors
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Localization
LANG = os.environ.get("LANG", "en_US")
IS_TR = "TR" in LANG.upper() or "TURKISH" in LANG.upper()

STRINGS = {
    "tr": {
        "config_err": "Hata: Config klasörü oluşturulamadı:",
        "data_err": "Hata: Veri dosyası oluşturulamadı:",
        "corrupt_err": "Uyarı: Proje dosyası bozuk, boş başlatılıyor.",
        "read_err": "Hata: Projeler okunamadı:",
        "save_err": "Hata: Projeler kaydedilemedi:",
        "path_warn": "[!] Uyarı: Yol bulunamadı ->",
        "launching": "-> Başlatılıyor:",
        "launch_err": "[!] Hata oluştu:",
        "input_cancel": "\n\nİşlem iptal edildi.\n",
        "new_proj_title": "--- Yeni Proje Oluştur ---",
        "proj_name_input": "Proje Adı: ",
        "name_exists": "Bu isimde bir proje zaten var!",
        "proj_created": "Proje '{}' oluşturuldu! Şimdi içine workspace ekleyelim...",
        "add_ws_title": "--- Çalışma Alanı Ekle: {} ---",
        "ws_name_input": "Çalışma Alanı Adı (örn: Backend, Frontend): ",
        "path_input": "Yol (Path): ",
        "path_create_prompt": "'{}' yok. Oluşturulsun mu? (e/h): ",
        "folder_created": "Klasör oluşturuldu.",
        "editor_input": "Editör/Komut (örn: code, idea): ",
        "ws_added": "Workspace '{}' eklendi!",
        "del_confirm": "DIKKAT: '{}' projesi ve tüm ayarları silinecek. Emin misin? (evet): ",
        "proj_deleted": "Proje '{}' silindi.",
        "ws_del_title": "--- Workspace Sil ({}) ---",
        "no_ws_del": "Silinecek workspace yok.",
        "back_opt": "BACK. Geri Dön",
        "del_num_input": "\nSilinecek numara: ",
        "ws_deleted": "'{}' silindi.",
        "invalid_sel": "Geçersiz seçim.",
        "help_title": "--- YARDIM VE REHBER ---",
        "help_vscode": "- VS Code Kullanımı: Editör kısmına 'code' yazın.",
        "help_idea": "- IntelliJ IDEA Kullanımı: Editör kısmına 'idea' yazın.",
        "help_idea_note": "  (Not: Command-line Launcher aktif olmalı.)",
        "help_android": "- Android Studio Kullanımı: Editör kısmına 'studio' yazın.",
        "help_specials": "- Özel Komutlar:",
        "help_back": "  - BACK: Bir önceki menüye döner.",
        "help_exit": "  - EXIT: Uygulamadan çıkar.",
        "help_all": "  - ALL START: Projedeki tüm çalışma alanlarını başlatır.",
        "help_mgmt": "  - ADD / REMOVE: Yönetim komutları.",
        "continue_key": "\nDevam etmek için Enter'a basın...",
        "proj_not_found": "Proje artık mevcut değil.",
        "proj_header": "Proje: ",
        "open_suffix": "AÇ",
        "cmds_header": "Komutlar:",
        "cmd_all": "ALL START   -> Tümünü Başlat",
        "cmd_add": "ADD         -> Workspace Ekle",
        "cmd_del": "DELETE      -> Workspace Sil",
        "cmd_rem": "REMOVE      -> Projeyi Sil",
        "cmd_back": "BACK        -> Geri Dön",
        "cmd_help": "HELP        -> Yardım",
        "choice_input": "Komut/No: ",
        "launching_all": "🚀 Tüm çalışma alanları başlatılıyor...",
        "no_projs": "   Henüz hiç proje yok kanka.",
        "add_hint": "   ADD ile yeni proje ekleyebilirsin.",
        "main_add": "ADD         -> Yeni Proje Ekle",
        "main_help": "HELP        -> Yardım Göster",
        "main_exit": "EXIT        -> Çıkış",
        "goodbye": "Görüşürüz kanka! 👋",
        "invalid_num": "Geçersiz numara."
    },
    "en": {
        "config_err": "Error: Could not create config dir:",
        "data_err": "Error: Could not create data file:",
        "corrupt_err": "Warning: Corrupt data file, starting empty.",
        "read_err": "Error reading projects:",
        "save_err": "Error saving projects:",
        "path_warn": "[!] Warning: Path not found ->",
        "launching": "-> Launching:",
        "launch_err": "[!] Error occurred:",
        "input_cancel": "\n\nOperation cancelled.\n",
        "new_proj_title": "--- Create New Project ---",
        "proj_name_input": "Project Name: ",
        "name_exists": "A project with this name already exists!",
        "proj_created": "Project '{}' created! Let's add a workspace...",
        "add_ws_title": "--- Add Workspace: {} ---",
        "ws_name_input": "Workspace Name (e.g. Backend, Frontend): ",
        "path_input": "Path: ",
        "path_create_prompt": "'{}' not found. Create? (y/n): ",
        "folder_created": "Directory created.",
        "editor_input": "Editor/Command (e.g. code, idea): ",
        "ws_added": "Workspace '{}' added!",
        "del_confirm": "WARNING: Project '{}' and settings will be deleted. Sure? (yes): ",
        "proj_deleted": "Project '{}' deleted.",
        "ws_del_title": "--- Delete Workspace ({}) ---",
        "no_ws_del": "No workspaces to delete.",
        "back_opt": "BACK. Go Back",
        "del_num_input": "\nNumber to delete: ",
        "ws_deleted": "'{}' deleted.",
        "invalid_sel": "Invalid selection.",
        "help_title": "--- HELP & GUIDE ---",
        "help_vscode": "- VS Code: Type 'code' as editor.",
        "help_idea": "- IntelliJ IDEA: Type 'idea' as editor.",
        "help_idea_note": "  (Note: Ensure Command-line Launcher is active.)",
        "help_android": "- Android Studio: Type 'studio' as editor.",
        "help_specials": "- Special Commands:",
        "help_back": "  - BACK: Go to previous menu.",
        "help_exit": "  - EXIT: Exit application.",
        "help_all": "  - ALL START: Launch all workspaces.",
        "help_mgmt": "  - ADD / REMOVE: Management commands.",
        "continue_key": "\nPress Enter to continue...",
        "proj_not_found": "Project no longer exists.",
        "proj_header": "Project: ",
        "open_suffix": "OPEN",
        "cmds_header": "Commands:",
        "cmd_all": "ALL START   -> Start All",
        "cmd_add": "ADD         -> Add Workspace",
        "cmd_del": "DELETE      -> Delete Workspace",
        "cmd_rem": "REMOVE      -> Delete Project",
        "cmd_back": "BACK        -> Go Back",
        "cmd_help": "HELP        -> Help",
        "choice_input": "Command/No: ",
        "launching_all": "🚀 Launching all workspaces...",
        "no_projs": "   No projects found yet, buddy.",
        "add_hint": "   Use ADD to create a new project.",
        "main_add": "ADD         -> Add New Project",
        "main_help": "HELP        -> Show Help",
        "main_exit": "EXIT        -> Exit",
        "goodbye": "See you later, buddy! 👋",
        "invalid_num": "Invalid number."
    }
}

def T(key, *args):
    """Helper for translation."""
    lang_dict = STRINGS["tr"] if IS_TR else STRINGS["en"]
    text = lang_dict.get(key, key)
    if args:
        return text.format(*args)
    return text

# --- Core Data Functions ---

def ensure_config_exists():
    """Config ve data dosyasının varlığından emin olur."""
    if not os.path.exists(CONFIG_DIR):
        try:
            os.makedirs(CONFIG_DIR)
        except OSError as e:
            print(f"{RED}{T('config_err')} {e}{RESET}")
            sys.exit(1)
    
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump({}, f)
        except IOError as e:
            print(f"{RED}{T('data_err')} {e}{RESET}")
            sys.exit(1)

def load_projects():
    """Projeleri JSON'dan yükler."""
    ensure_config_exists()
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        print(f"{RED}{T('corrupt_err')}{RESET}")
        return {}
    except IOError as e:
        print(f"{RED}{T('read_err')} {e}{RESET}")
        sys.exit(1)

def save_projects(projects):
    """Projeleri JSON'a kaydeder."""
    ensure_config_exists()
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(projects, f, indent=4)
    except IOError as e:
        print(f"{RED}{T('save_err')} {e}{RESET}")
        sys.exit(1)

def resolve_path(path):
    """Yolu absolite path'e çevirir."""
    return os.path.abspath(os.path.expanduser(path))

# --- Helper Logic ---

def print_banner():
    """Havalı ASCII Banner'ı yazdırır."""
    print(GREEN)
    print(r"""
  _ _ _ __  __ 
 | | | |  \/  |
 | | | | |\/| | v1.0.0
 | | | | |  | |
  \___/|_|  |_| Workspace Manager
""")
    print(RESET)
    print(f"  > Dev: Haşim Özer [Full Stack Developer]")
    print(f"  > Web: hasimozer.com")
    print("-" * 50)

def clear_screen():
    """Ekranı temizler ve banner'ı basar."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

def launch_cmd(cmd, path):
    """Verilen komutu ve yolu arka planda çalıştırır."""
    if not os.path.exists(path):
        print(f"  {RED}{T('path_warn')} {path}{RESET}")
        return False
    
    print(f"  {CYAN}{T('launching')} {cmd} @ {path}{RESET}")
    try:
        subprocess.Popen(f"{cmd} {path}", shell=True,
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         start_new_session=True)
        return True
    except Exception as e:
        print(f"  {RED}{T('launch_err')} {e}{RESET}")
        return False

# --- Menu Flows ---

def get_input(prompt_text):
    """Güvenli input alma ve renkli prompt."""
    try:
        # Prompt text itself can have colors, but input cursor should be generic
        return input(f"{BOLD}{prompt_text}{RESET}").strip()
    except (KeyboardInterrupt, EOFError):
        print(T("input_cancel"))
        return None

def add_new_project_flow(projects):
    """Yeni ana proje ekleme akışı."""
    print(f"\n{BLUE}{T('new_proj_title')}{RESET}")
    while True:
        name = get_input(T("proj_name_input"))
        if not name: return
        if name.upper() == "BACK": return

        if name in projects:
            print(f"  {RED}{T('name_exists')}{RESET}")
            continue
        break
    
    projects[name] = {"workspaces": []}
    save_projects(projects)
    print(f"{GREEN}{T('proj_created', name)}{RESET}")
    add_workspace_flow(projects, name)

def add_workspace_flow(projects, project_name):
    """Projeye yeni workspace ekleme akışı."""
    print(f"\n{BLUE}{T('add_ws_title', project_name)}{RESET}")
    
    ws_name = get_input(T("ws_name_input"))
    if not ws_name or ws_name.upper() == "BACK": return

    path_raw = get_input(T("path_input"))
    if not path_raw or path_raw.upper() == "BACK": return
    path = resolve_path(path_raw)
    
    if not os.path.exists(path):
        create = get_input(f"  {T('path_create_prompt', path)}")
        if create and create.lower() in ['e', 'y']:
            os.makedirs(path, exist_ok=True)
            print(f"  {GREEN}{T('folder_created')}{RESET}")
    
    cmd = get_input(T("editor_input"))
    if not cmd: cmd = "code"

    new_ws = {"name": ws_name, "path": path, "cmd": cmd}
    projects[project_name]["workspaces"].append(new_ws)
    save_projects(projects)
    print(f"{GREEN}{T('ws_added', ws_name)}{RESET}")
    time.sleep(1)

def delete_project_flow(projects, project_name):
    """Projeyi silme."""
    confirm = get_input(f"{RED}{T('del_confirm', project_name)}{RESET}")
    if confirm in ["evet", "yes"]:
        del projects[project_name]
        save_projects(projects)
        print(f"{YELLOW}{T('proj_deleted', project_name)}{RESET}")
        time.sleep(1)
        return True # Deleted
    return False

def delete_workspace_flow(projects, project_name):
    """Workspace silme."""
    while True:
        clear_screen()
        workspaces = projects[project_name]["workspaces"]
        if not workspaces:
            print(f"{YELLOW}{T('no_ws_del')}{RESET}")
            time.sleep(1)
            return

        print(f"\n{BLUE}{T('ws_del_title', project_name)}{RESET}")
        for idx, ws in enumerate(workspaces, 1):
            print(f"{BLUE}{idx}.{RESET} {ws['name']}")
        
        print(f"\n{YELLOW}{T('back_opt')}{RESET}")
        sel = get_input(T("del_num_input"))
        
        if not sel: continue
        if sel.upper() == "BACK": return
        
        if not sel.isdigit(): continue
        
        idx = int(sel) - 1
        
        if 0 <= idx < len(workspaces):
            removed = workspaces.pop(idx)
            save_projects(projects)
            print(f"{YELLOW}{T('ws_deleted', removed['name'])}{RESET}")
            time.sleep(1)
        else:
            print(f"{RED}{T('invalid_sel')}{RESET}")
            time.sleep(1)

def show_help():
    """Yardım ekranını gösterir."""
    clear_screen()
    print(f"\n{BLUE}{T('help_title')}{RESET}")
    print(f"{T('help_vscode')}")
    print(f"{T('help_idea')}")
    print(f"{T('help_idea_note')}")
    print(f"{T('help_android')}")
    print(f"{T('help_specials')}")
    print(f"{YELLOW}{T('help_back')}{RESET}")
    print(f"{YELLOW}{T('help_exit')}{RESET}")
    print(f"{YELLOW}{T('help_all')}{RESET}")
    print(f"{YELLOW}{T('help_mgmt')}{RESET}")
    
    get_input(T("continue_key"))

def project_menu(projects, project_name):
    """Proje detay menüsü."""
    while True:
        clear_screen()
        if project_name not in projects:
            print(f"{RED}{T('proj_not_found')}{RESET}")
            time.sleep(1)
            break
            
        data = projects[project_name]
        workspaces = data.get("workspaces", [])

        print(f"\n{T('proj_header')}{BLUE}{project_name}{RESET}")
        
        # List workspaces
        for idx, ws in enumerate(workspaces, 1):
            print(f"{BLUE}{idx}.{RESET} {ws['name']} {CYAN}{T('open_suffix')}{RESET} ({ws['cmd']})")
        
        print("-" * 20)
        print(f"{BOLD}{T('cmds_header')}{RESET}")
        print(f"  {YELLOW}{T('cmd_all')}{RESET}")
        print(f"  {YELLOW}{T('cmd_add')}{RESET}")
        print(f"  {YELLOW}{T('cmd_del')}{RESET}")
        print(f"  {YELLOW}{T('cmd_rem')}{RESET}")
        print(f"  {YELLOW}{T('cmd_back')}{RESET}")
        print(f"  {YELLOW}{T('cmd_help')}{RESET}")
        
        choice = get_input(f"\n{project_name} > {T('choice_input')}")
        
        if not choice: continue
        
        # Mapping localized commands back to internal commands logic
        # For simplicity in this v1.0.0, we keep internal commands English (BACK, EXIT)
        # but display can be localized. The user must type standard commands.
        # Or we can check translated strings:
        cmd = choice.upper()
        
        # TODO: Better command mapping for localization
        # Currently keeping static English commands for robustness
        
        if cmd == 'BACK':
            break
        elif cmd == 'HELP':
             show_help()
        elif cmd == 'ALL START':
            print(f"{CYAN}{T('launching_all')}{RESET}")
            for ws in workspaces:
                launch_cmd(ws['cmd'], ws['path'])
                time.sleep(0.5)
            get_input(T("continue_key"))
        elif cmd == 'ADD':
            add_workspace_flow(projects, project_name)
        elif cmd == 'DELETE':
            delete_workspace_flow(projects, project_name)
        elif cmd == 'REMOVE':
            if delete_project_flow(projects, project_name):
                break
        elif choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(workspaces):
                ws = workspaces[idx-1]
                launch_cmd(ws['cmd'], ws['path'])
            else:
                print(f"{RED}{T('invalid_num')}{RESET}")
                time.sleep(1)

def main_menu():
    """Ana menü döngüsü."""
    while True:
        clear_screen()
        projects = load_projects()
        project_names = list(projects.keys())
        
        if not project_names:
            print(f"\n{T('no_projs')}")
            print(f"{T('add_hint')}")
        else:
            for idx, name in enumerate(project_names, 1):
                ws_count = len(projects[name].get("workspaces", []))
                print(f"{BLUE}{idx}.{RESET} {name} ({ws_count} alan)")

        print("-" * 20)
        print(f"{BOLD}{T('cmds_header')}{RESET}")
        print(f"  {YELLOW}{T('main_add')}{RESET}")
        print(f"  {YELLOW}{T('main_help')}{RESET}")
        print(f"  {YELLOW}{T('main_exit')}{RESET}")
        
        choice = get_input(f"\nAna Menü > {T('choice_input')}")
        
        if not choice: continue
        
        cmd = choice.upper()
        
        if cmd == 'EXIT':
            clear_screen()
            print(f"{GREEN}{T('goodbye')}{RESET}")
            break
        elif cmd == 'HELP':
            show_help()
        elif cmd == 'ADD':
            add_new_project_flow(projects)
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(project_names):
                selected_project = project_names[idx]
                project_menu(projects, selected_project)
            else:
                print(f"{RED}{T('invalid_num')}{RESET}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{RED}Çıkış yapılıyor...{RESET}")
