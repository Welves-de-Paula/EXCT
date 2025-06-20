const { Client, LocalAuth } = require('whatsapp-web.js');
const fs = require('fs');
const qrcode = require('qrcode-terminal');
const path = require('path');
const express = require('express');

const app = express();
const PORT = 3000;

const client = new Client({
  authStrategy: new LocalAuth()
});

// Função para formatar epoch em data/hora legível
function formatEpoch(epoch) {
  const date = new Date(epoch * 1000); // Multiplica por 1000 porque o epoch está em segundos
  const dia = date.getDate().toString().padStart(2, '0');
  const mes = (date.getMonth() + 1).toString().padStart(2, '0'); // Janeiro é 0
  const ano = date.getFullYear();
  const horas = date.getHours().toString().padStart(2, '0');
  const minutos = date.getMinutes().toString().padStart(2, '0');
  const segundos = date.getSeconds().toString().padStart(2, '0');

  return `${dia}/${mes}/${ano} ${horas}:${minutos}:${segundos}`;
}

let chatsCache = [];
let messagesCache = {};

client.on('qr', (qr) => {
  console.log('Escaneie este QR code no WhatsApp:');
  qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
  console.log('Cliente conectado!');
  // Carrega os chats na inicialização
  chatsCache = await client.getChats();
  console.log(`Total de chats encontrados: ${chatsCache.length}`);
});

function sanitizeFileName(nome) {
  return nome.replace(/[<>:"/\\|?*\x00-\x1F]/g, '_').slice(0, 50);
}

// Rota para exportar mensagens para arquivos
app.get('/download', async (req, res) => {
  if (!chatsCache.length) {
    return res.status(503).json({ error: 'Chats ainda não carregados.' });
  }
  const dir = 'messages';
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
  }
  for (let i = 0; i < chatsCache.length; i++) {
    const chat = chatsCache[i];
    const telefone = sanitizeFileName(chat.id.user || 'desconhecido');
    const filePath = path.join(dir, `${telefone}.txt`);
    try {
      const mensagens = await chat.fetchMessages({ limit: 1000 });
      const conteudo = mensagens.map(msg => {
        const autor = msg.author || msg.from;
        const corpo = msg.body;
        const data = formatEpoch(msg.timestamp);
        return `${data} | ${autor}: ${corpo}`;
      }).join('\n');
      fs.writeFileSync(filePath, conteudo, 'utf-8');
    } catch (e) {
      // Ignora erros individuais
    }
  }
  res.json({ status: 'Mensagens exportadas para arquivos.' });
});

// Lista todos os chats (apenas id e nome)
app.get('/chats', (req, res) => {
  if (!chatsCache.length) {
    return res.status(503).json({ error: 'Chats ainda não carregados.' });
  }
  const lista = chatsCache.map(chat => ({
    id: chat.id._serialized,
    name: chat.name || chat.id.user
  }));
  res.json(lista);
});

// Lista mensagens de um chat específico
app.get('/chats/:id', async (req, res) => {
  const chatId = req.params.id;
  const chat = chatsCache.find(c => c.id._serialized === chatId);
  if (!chat) {
    return res.status(404).json({ error: 'Chat não encontrado.' });
  }
  try {
    if (!messagesCache[chatId]) {
      // Limite de 1000 mensagens para evitar sobrecarga
      const mensagens = await chat.fetchMessages({ limit: 1000 });
      messagesCache[chatId] = mensagens.map(msg => ({
        ...msg,
        timestamp: formatEpoch(msg.timestamp)
      }));
    }
    res.json(messagesCache[chatId]);
  } catch (e) {
    res.status(500).json({ error: 'Erro ao buscar mensagens.' });
  }
});

app.get('/send', async (req, res) => {
  const chatId = '120363400680237313@g.us';
  // const mentionNumber = '553391147649'; // só o número limpo
  const mensagem = 'Aooo CAFÉEEEEEEEEE';

  for (let i = 0; i < 5; i++) {

    try {


      const chat = await client.getChatById(chatId);

      await chat.sendMessage(mensagem);

      res.json({ status: 'Mensagem enviada com sucesso.' });
    } catch (e) {
      console.error(e);
      res.status(500).json({ error: e.toString() });
    }
  }
});


/*
Como iniciar:

1. Instale as dependências (caso ainda não tenha):
   npm install express whatsapp-web.js qrcode-terminal

2. Execute o script:
   node baixarConversas.js

3. Abra o navegador e acesse:
   http://localhost:3000/chats         - Lista todos os chats
   http://localhost:3000/chats/:id     - Lista mensagens de um chat (substitua :id pelo id do chat)
   http://localhost:3000/download      - Exporta mensagens para arquivos

No primeiro uso, será necessário escanear o QR code exibido no terminal com o WhatsApp.
*/

// Inicializa o WhatsApp e o servidor Express
client.initialize().catch(err => console.error('Erro na inicialização:', err));

app.listen(PORT, () => {
  console.log(`API rodando em http://localhost:${PORT}`);
});
