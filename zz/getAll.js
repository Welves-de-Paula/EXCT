const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

console.log('\n');
console.log('Bem-vindo ao WhatsApp Backup!');
console.log('Powered by Welves de Paula');
console.log('\n');

const client = new Client({
  authStrategy: new LocalAuth()
});

const MILIS_5_ANOS = 1000 * 60 * 60 * 24 * 365 * 5;

function formatEpoch(epoch) {
  const date = new Date(epoch * 1000);
  const dia = date.getDate().toString().padStart(2, '0');
  const mes = (date.getMonth() + 1).toString().padStart(2, '0');
  const ano = date.getFullYear();
  const horas = date.getHours().toString().padStart(2, '0');
  const minutos = date.getMinutes().toString().padStart(2, '0');
  const segundos = date.getSeconds().toString().padStart(2, '0');
  return `${dia}/${mes}/${ano} ${horas}:${minutos}:${segundos}`;
}

function dataLimiteTimestamp() {
  const agora = Date.now();
  return Math.floor((agora - MILIS_5_ANOS) / 1000); // segundos
}

client.on('qr', (qr) => {
  console.log('Escaneie este QR code no WhatsApp:');
  qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
  console.log('Cliente conectado!', [new Date().toLocaleTimeString()]);

  let chats = await client.getChats();
  chats = chats.filter(chat => !chat.isBroadcast);

  console.log(`Total de chats encontrados: ${chats.length} `, [new Date().toLocaleTimeString()]);
  console.log('Iniciando o processamento dos chats...\n');

  const dataLimite = dataLimiteTimestamp();
  const items = [];

  for (let i = 0; i < chats.length; i++) {
    const chat = chats[i];
    try {
      console.log(`Buscando mensagens de: ${chat.name || chat.id.user}`);

      const todasMensagens = await chat.fetchMessages({ limit: 999999999 });

      const mensagens = todasMensagens
        .filter(msg => msg.timestamp >= dataLimite)
        .map(msg => ({
          author: msg.author || msg.from,
          body: msg.body,
          timestamp: formatEpoch(msg.timestamp)
        }));

      if (mensagens.length > 0) {
        items.push({
          name: chat.name || chat.id.user,
          phone: chat.id.user,
          mensagens
        });
      }

    } catch (erro) {
      console.error(`Erro ao processar o chat ${chat.name || chat.id.user}:`, erro);
    }
  }

  fs.writeFileSync('mensagens2.json', JSON.stringify(items, null, 2), 'utf8');
  console.log('\nProcessamento concluído. Mensagens salvas em "mensagens.json".');
  process.exit(0);
});

client.initialize();
