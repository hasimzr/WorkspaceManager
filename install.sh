#!/bin/bash

INSTALL_DIR="$HOME/.WorkspaceManager"
SCRIPT_URL="https://raw.githubusercontent.com/hasimozer/WorkspaceManager/main/WorkspaceManager.py"
LOCAL_SCRIPT="$INSTALL_DIR/WorkspaceManager.py"

# Renkler
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}>>> WorkspaceManager v1.0.0 Kurulumu Başlatılıyor...${NC}"

# 1. Klasör Oluştur
if [ ! -d "$INSTALL_DIR" ]; then
  echo "--- Klasör oluşturuluyor: $INSTALL_DIR"
  mkdir -p "$INSTALL_DIR"
fi

# 2. Dosyayı Kopyala (Lokalden veya İndirerek - GitHub dağıtımı için indirme mantığı kilitliyorum)
# Şimdilik local workspace'ten alıyormuş gibi varsayıyoruz ama release için curl kullanılır.
# echo "--- WorkspaceManager indiriliyor..."
# curl -sL $SCRIPT_URL -o $LOCAL_SCRIPT
# LOCAL dağıtım simülasyonu için mevcut dosyayı kopyalıyoruz:
cp WorkspaceManager.py "$LOCAL_SCRIPT"

chmod +x "$LOCAL_SCRIPT"
echo -e "${GREEN}✔ WorkspaceManager kopyalandı.${NC}"

# 3. Alias Ekleme
SHELL_CFG=""
if [ -n "$ZSH_VERSION" ]; then
  SHELL_CFG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
  SHELL_CFG="$HOME/.bashrc"
else
  # Fallback
  SHELL_CFG="$HOME/.bash_profile"
fi

ALIAS_CMD="alias p='python3 $LOCAL_SCRIPT'"

if grep -Fxq "$ALIAS_CMD" "$SHELL_CFG"; then
    echo "--- Alias zaten mevcut."
else
    echo "--- Alias ekleniyor: $SHELL_CFG"
    echo "" >> "$SHELL_CFG"
    echo "# WorkspaceManager CLI shortcut" >> "$SHELL_CFG"
    echo "$ALIAS_CMD" >> "$SHELL_CFG"
    echo "alias WorkspaceManager='python3 $LOCAL_SCRIPT'" >> "$SHELL_CFG"
fi

echo -e "${GREEN}>>> Kurulum Tamamlandı! 🚀${NC}"
echo "Lütfen terminalinizi yeniden başlatın veya şu komutu çalıştırın:"
echo -e "${BLUE}source $SHELL_CFG${NC}"
echo "Kullanım: 'p' veya 'WorkspaceManager' yazarak başlatabilirsiniz."
