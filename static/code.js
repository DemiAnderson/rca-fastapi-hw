async function castVote(cardId) {
    const response = await fetch('/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ card_id: cardId })
    });
    if (response.redirected) {
        window.location.href = response.url;
    }
}
