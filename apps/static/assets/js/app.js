class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;
        const chatbotButton = document.getElementById('chatbot-button');

        this.prompt(chatBox)

        chatbotButton.addEventListener('click', () => this.toggleState(chatBox))
        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('.chat_user');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    prompt(chatbox) {
        this.messages.push({ name: "Bot", message: "Selamat Datang di StuBot! Mari ajukan pertanyaan stunting di sini!" });
        this.updateChatText(chatbox)

        const buttonsContainer = document.createElement('div');
        buttonsContainer.classList.add('flex', 'justify-center');

        const button1 = document.createElement('button');
        button1.classList.add('bg-[#00b202]', 'hover:bg-green-700', 'text-white', 'font-medium', 'text-xs', 'py-1', 'px-2', 'rounded', 'mr-1', 'my-1');
        button1.textContent = 'Tentang StuBot';
        button1.addEventListener('click', () => {
            this.messages.push({ name: "User", message: "Tentang StuBot" });
            this.messages.push({ name: "Bot", message: "StuBot merupakan bot yang dapat melayani pertanyaan umum tentang stunting ya! Adapun informasi yang dapat disampaikan meliputi informasi stunting meliputi pengertian, ciri, pencegahan, dampak, perbedaan dengan pendek, serta tentang ASI, MPASI, tanda bayi yang lapar, data stunting di Kalimantan Barat dan lain-lain." });
            this.updateChatText(chatbox);
        });

        const button2 = document.createElement('button');
        button2.classList.add('bg-[#00b202]', 'hover:bg-green-700', 'text-white', 'font-medium', 'text-xs', 'py-1', 'px-2', 'rounded', 'mr-1', 'my-1');
        button2.textContent = 'Contoh Pertanyaan';
        button2.addEventListener('click', () => {
            this.messages.push({ name: "User", message: "Contoh Pertanyaan" });
            this.messages.push({ name: "Bot", message: "Contoh pertanyaan yang dapat kamu ajukan seperti: 1. Apa sih pengertian dari stunting? 2. Apa saja ciri-ciri dari anak stunting? 3. Bagaimana Perbedaan Pendek dan Stunting? Kamu juga dapat mengajukan pertanyaan lainnya seputar stunting loh!" });
            this.updateChatText(chatbox);            
        });

        const button3 = document.createElement('button');
        button3.classList.add('bg-[#00b202]', 'hover:bg-green-700', 'text-white', 'font-medium', 'text-xs', 'py-1', 'px-2', 'rounded', 'my-1');
        button3.textContent = 'Pertanyaan Lain';
        button3.addEventListener('click', () => {
            this.messages.push({ name: "User", message: "Pertanyaan Lain" });
            this.messages.push({ name: "Bot", message: "Jika kamu ingin mengajukan pertanyaan lainnya yang belum dapat dijawab oleh StuBot, kamu bisa menuju ke menu kontak untuk mengajukan pertanyaan lewat email atau sosial media IDAI kalbar ya!" });
            this.updateChatText(chatbox);            
        });

        buttonsContainer.append(button1, button2, button3);
        chatbox.querySelector('.chatbox__btns').append(buttonsContainer);
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var csrf_token = "{{ csrf_token() }}";
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
        // consider changing local host here if required. /predict needs to be there.
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrf_token
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Bot", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Bot")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();