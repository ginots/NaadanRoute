$(document).ready(function() {
    scrollChat();
    setTimeout(() => {
        $("#chat-teaser").css({"opacity": "1", "transform": "translateX(-10px)"});
    }, 3000);

    $("#chat-circle").click(function(e) {
        e.stopPropagation();
        $("#chat-window-element").removeClass('d-none');
        $("#chat-teaser").fadeOut();
        scrollChat();
    });

    $("#chat-box-toggle").click(function(e) {
        e.stopPropagation();
        $("#chat-window-element").addClass('d-none');
    });

    $(document).click(function(event) {
        const $win = $("#chat-window-element");
        if (!$win.hasClass('d-none') && !$win.is(event.target) && $win.has(event.target).length === 0 && !$("#chat-circle").is(event.target)) {
            $win.addClass('d-none');
        }
    });

    // --- SEND LOGIC ---
    $("#chat-submit").click(() => sendToKera());
    $("#chat-input").on('keypress', (e) => { if(e.which == 13) sendToKera(); });
});

async function sendToKera() {
    const inputField = $("#chat-input");
    const input = inputField.val().trim();
    if (!input) return;

    $("#chat-logs").append(`<div class="user-msg">${input}</div>`);
    inputField.val('');
    scrollChat();

    toggleLoading(true);

    try {
        const response = await fetch('/tours/ai_chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ message: input })
        });

        const data = await response.json();
        toggleLoading(false);

        // Typewriter effect for Kera
        typeWriter(data.reply, "bot-msg");

        if (data.package_id) {
            setTimeout(() => {
                window.location.href = `/tours/tours_dashboard/?recommended=${data.package_id}#personal-tour`;
            }, 3000);
        }
    } catch (error) {
        toggleLoading(false);
        $("#chat-logs").append(`<div class="bot-msg">Sorry, I'm having trouble connecting.</div>`);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    if (window.location.hash === "#personal-tour") {
        setTimeout(() => {
            const element = document.getElementById("personal-tour");
            if (element) {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });

                element.style.borderRadius = "20px";
                element.style.boxShadow = "0 0 0 1px #28a745";
                setTimeout(() => { element.style.boxShadow = "none"; }, 1000);
            }
        }, 600);
    }
});


function typeWriter(text, className) {
    const chatLogs = $("#chat-logs");
    const messageDiv = $(`<div class="${className}"></div>`);
    chatLogs.append(messageDiv);

    let i = 0;
    function type() {
        if (i < text.length) {
            messageDiv.append(text.charAt(i));
            i++;
            scrollChat();
            setTimeout(type, 30);
        }
    }
    type();
}

function toggleLoading(show) {
    $("#kera-typing").remove();
    if (show) {
        $("#chat-logs").append(`<div id="kera-typing" class="typing"><span></span><span></span><span></span></div>`);
        scrollChat();
    }
}

function scrollChat() {
    const logs = document.getElementById('chat-logs');
    if (logs) {
        window.requestAnimationFrame(() => {
            logs.scrollTop = logs.scrollHeight;
        });
    }
}
