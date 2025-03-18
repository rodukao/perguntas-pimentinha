// src/pages/AddQuestion.js
import React, { useState } from 'react';
import axios from 'axios';

function AddQuestion() {
  const [level, setLevel] = useState(1);
  const [question, setQuestion] = useState('');

  const handleClickPepper = (selectedLevel) => {
    setLevel(selectedLevel);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!question.trim()) {
      alert('Digite uma pergunta antes de enviar.');
      return;
    }

    try {
      // Ajuste a URL se seu backend estiver rodando em outro lugar
      const response = await axios.post('http://localhost:5000/add_question', {
        level,
        question
      });
      alert(response.data.message);
      // Limpa o form
      setQuestion('');
      setLevel(1);
    } catch (error) {
      console.error(error);
      alert('Erro ao enviar pergunta');
    }
  };

  return (
    <div>
      <h2>Adicionar Pergunta</h2>

      {/* Exibir 5 pimentas (cliques) */}
      <div style={{ display: 'flex', marginBottom: '1rem' }}>
        {[1, 2, 3, 4, 5].map((lvl) => {
          const pepperImg = lvl <= level
            ? '/images/red-pepper.png'  // Se você tiver essas imagens na pasta public/images/
            : '/images/gray-pepper.png';

          return (
            <img
              key={lvl}
              src={pepperImg}
              alt={lvl <= level ? 'Pimenta Vermelha' : 'Pimenta Cinza'}
              style={{
                width: '40px',
                cursor: 'pointer',
                marginRight: '5px'
              }}
              onClick={() => handleClickPepper(lvl)}
            />
          );
        })}
      </div>

      <form onSubmit={handleSubmit}>
        <label>Pergunta:</label>
        <br />
        <textarea
          rows="4"
          cols="50"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <br />
        <button type="submit">Enviar Pergunta</button>
      </form>
    </div>
  );
}

export default AddQuestion;
