(() => {
  "use strict";

  const STORAGE_KEY = "gh900.progress.v1";
  const $ = (id) => document.getElementById(id);

  // ---------- Armazenamento local ----------
  const emptyState = () => ({ read: {}, stats: {}, wrong: [], cards: {} });

  function loadState() {
    try {
      const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY));
      return { ...emptyState(), ...(parsed && typeof parsed === "object" ? parsed : {}) };
    } catch {
      return emptyState();
    }
  }

  function saveState(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {
      /* armazenamento indisponível: o app continua funcionando sem salvar */
    }
  }

  function recordResult(topic, id, correct) {
    const state = loadState();
    const entry = state.stats[topic] || { answered: 0, correct: 0 };
    entry.answered += 1;
    if (correct) entry.correct += 1;
    state.stats[topic] = entry;
    state.wrong = state.wrong.filter((w) => w !== id);
    if (!correct) state.wrong.push(id);
    saveState(state);
  }

  function el(tag, props = {}, children = []) {
    const node = document.createElement(tag);
    Object.assign(node, props);
    for (const child of [].concat(children)) {
      node.append(child instanceof Node ? child : document.createTextNode(child));
    }
    return node;
  }

  async function fetchJson(url, options) {
    const response = await fetch(url, options);
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || "Falha na requisição.");
    return data;
  }

  // ---------- Início ----------
  function initIndex() {
    const state = loadState();
    let answered = 0;
    let correct = 0;
    for (const [slug, stat] of Object.entries(state.stats)) {
      answered += stat.answered;
      correct += stat.correct;
      const bar = document.querySelector(`[data-bar="${slug}"]`);
      const status = document.querySelector(`[data-status="${slug}"]`);
      const pct = stat.answered ? Math.round((stat.correct / stat.answered) * 100) : 0;
      if (bar) bar.style.width = `${pct}%`;
      if (status) status.textContent = `${pct}% de acerto em ${stat.answered} respostas`;
    }
    $("stat-answered").textContent = answered;
    $("stat-accuracy").textContent = answered ? `${Math.round((correct / answered) * 100)}%` : "–";
    const total = (id) => Number($(id).textContent.split("/")[1]);
    $("stat-read").textContent = `${Object.keys(state.read).length}/${total("stat-read")}`;
    $("stat-cards").textContent = `${Object.keys(state.cards).length}/${total("stat-cards")}`;
  }

  // ---------- Tópico ----------
  function initTopic() {
    const slug = $("topic").dataset.topic;
    const button = $("mark-read");
    const render = () => {
      const done = Boolean(loadState().read[slug]);
      button.textContent = done ? "✓ Lido (desmarcar)" : "Marcar como lido";
      button.classList.toggle("primary", !done);
    };
    button.addEventListener("click", () => {
      const state = loadState();
      if (state.read[slug]) delete state.read[slug];
      else state.read[slug] = true;
      saveState(state);
      render();
    });
    render();
  }

  // ---------- Cartões ----------
  function initFlashcards() {
    const params = new URLSearchParams(location.search);
    const topicSelect = $("card-topic");
    const known = $("card-pending");
    let cards = [];
    let deck = [];
    let index = 0;
    let flipped = false;

    const shuffle = (list) => {
      const copy = [...list];
      for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copy[i], copy[j]] = [copy[j], copy[i]];
      }
      return copy;
    };

    function buildDeck() {
      const state = loadState();
      deck = cards.filter((c) => !known.checked || !state.cards[c.id]);
      index = Math.min(index, Math.max(deck.length - 1, 0));
    }

    function render() {
      const state = loadState();
      const card = deck[index];
      const total = cards.length;
      const mastered = cards.filter((c) => state.cards[c.id]).length;
      $("card-counter").textContent = card
        ? `Cartão ${index + 1} de ${deck.length} · ${mastered}/${total} dominados`
        : `Nenhum cartão para mostrar · ${mastered}/${total} dominados`;
      $("card-label").textContent = flipped ? "Definição" : "Termo";
      $("card-text").textContent = card ? (flipped ? card.definition : card.term) : "🎉 Tudo dominado!";
      $("flashcard").classList.toggle("flipped", flipped);
    }

    const go = (step) => {
      if (!deck.length) return;
      index = (index + step + deck.length) % deck.length;
      flipped = false;
      render();
    };

    function mark(isKnown) {
      const card = deck[index];
      if (!card) return;
      const state = loadState();
      if (isKnown) state.cards[card.id] = true;
      else delete state.cards[card.id];
      saveState(state);
      if (known.checked && isKnown) {
        buildDeck();
        flipped = false;
        render();
      } else {
        go(1);
      }
    }

    async function load() {
      const topic = topicSelect.value;
      cards = await fetchJson(`/api/cartoes${topic ? `?topico=${encodeURIComponent(topic)}` : ""}`);
      index = 0;
      flipped = false;
      buildDeck();
      render();
    }

    $("flashcard").addEventListener("click", () => {
      flipped = !flipped;
      render();
    });
    $("card-prev").addEventListener("click", () => go(-1));
    $("card-next").addEventListener("click", () => go(1));
    $("card-known").addEventListener("click", () => mark(true));
    $("card-review").addEventListener("click", () => mark(false));
    $("card-shuffle").addEventListener("click", () => {
      cards = shuffle(cards);
      index = 0;
      flipped = false;
      buildDeck();
      render();
    });
    known.addEventListener("change", () => {
      buildDeck();
      render();
    });
    topicSelect.addEventListener("change", load);
    document.addEventListener("keydown", (event) => {
      if (["INPUT", "SELECT", "TEXTAREA"].includes(event.target.tagName)) return;
      if (event.key === "ArrowRight") go(1);
      else if (event.key === "ArrowLeft") go(-1);
      else if (event.key === " " && event.target.id !== "flashcard") {
        event.preventDefault();
        flipped = !flipped;
        render();
      }
    });

    if (params.get("topico")) topicSelect.value = params.get("topico");
    load().catch((error) => ($("card-counter").textContent = error.message));
  }

  // ---------- Questões ----------
  function initQuiz() {
    const params = new URLSearchParams(location.search);
    const setup = $("quiz-setup");
    const run = $("quiz-run");
    const resultBox = $("quiz-result");
    const topicNames = Object.fromEntries(
      [...$("quiz-topic").options].filter((o) => o.value).map((o) => [o.value, o.textContent.replace(/\s*\(\d+\)$/, "")])
    );

    let mode = "practice";
    let questions = [];
    let index = 0;
    let selections = {}; // id -> array de índices
    let results = {}; // id -> resposta corrigida do servidor

    if (params.get("topico")) $("quiz-topic").value = params.get("topico");
    $("retry-wrong").hidden = loadState().wrong.length === 0;

    const show = (section) => {
      setup.hidden = section !== setup;
      run.hidden = section !== run;
      resultBox.hidden = section !== resultBox;
    };

    async function start(url) {
      $("setup-error").hidden = true;
      try {
        questions = await fetchJson(url);
        if (!questions.length) throw new Error("Nenhuma questão encontrada para esse filtro.");
      } catch (error) {
        $("setup-error").textContent = error.message;
        $("setup-error").hidden = false;
        return;
      }
      mode = $("quiz-mode").value;
      index = 0;
      selections = {};
      results = {};
      show(run);
      renderQuestion();
    }

    $("setup-form").addEventListener("submit", (event) => {
      event.preventDefault();
      const size = Math.max(1, Math.min(50, Number($("quiz-size").value) || 10));
      const query = new URLSearchParams({ n: size });
      if ($("quiz-topic").value) query.set("topico", $("quiz-topic").value);
      start(`/api/questoes?${query}`);
    });

    $("retry-wrong").addEventListener("click", () => {
      const ids = loadState().wrong.join(",");
      start(`/api/questoes?n=50&ids=${ids}`);
    });

    function renderQuestion() {
      const question = questions[index];
      const result = results[question.id];
      const picked = new Set(selections[question.id] || []);
      $("quiz-progress").textContent = `Questão ${index + 1} de ${questions.length}`;
      $("quiz-tag").textContent = topicNames[question.topic] || question.topic;
      $("question-text").textContent = question.text;
      $("question-hint").textContent = question.choose > 1 ? `Selecione ${question.choose} respostas.` : "Selecione uma resposta.";

      const form = $("options");
      form.replaceChildren();
      question.options.forEach((option, i) => {
        const input = el("input", {
          type: question.choose > 1 ? "checkbox" : "radio",
          name: "option",
          value: String(i),
          checked: picked.has(i),
          disabled: Boolean(result),
        });
        const label = el("label", { className: "option" }, [input, el("span", {}, option)]);
        if (result) {
          if (result.answer.includes(i)) label.classList.add("right");
          else if (picked.has(i)) label.classList.add("wrong");
        }
        form.append(label);
      });

      const feedback = $("feedback");
      feedback.hidden = !(result && mode === "practice");
      if (!feedback.hidden) {
        feedback.className = `feedback ${result.correct ? "ok" : "bad"}`;
        feedback.replaceChildren(
          el("strong", {}, result.correct ? "Correto! " : "Incorreto. "),
          result.explanation
        );
      }

      const last = index === questions.length - 1;
      const practice = mode === "practice";
      $("btn-prev").hidden = practice || index === 0;
      $("btn-check").hidden = !practice || Boolean(result);
      $("btn-next").hidden = last || (practice && !result);
      $("btn-finish").hidden = !(last && (practice ? Boolean(result) : true));
    }

    $("options").addEventListener("change", () => {
      const question = questions[index];
      selections[question.id] = [...$("options").querySelectorAll("input:checked")].map((i) => Number(i.value));
    });

    async function grade(ids) {
      const answers = Object.fromEntries(ids.map((id) => [id, selections[id] || []]));
      return fetchJson("/api/corrigir", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers }),
      });
    }

    $("btn-check").addEventListener("click", async () => {
      const question = questions[index];
      if (!(selections[question.id] || []).length) {
        $("question-hint").textContent = "Escolha ao menos uma opção antes de verificar.";
        return;
      }
      const graded = await grade([question.id]);
      results[question.id] = graded[question.id];
      recordResult(question.topic, question.id, graded[question.id].correct);
      renderQuestion();
    });

    $("btn-next").addEventListener("click", () => {
      index += 1;
      renderQuestion();
    });
    $("btn-prev").addEventListener("click", () => {
      index -= 1;
      renderQuestion();
    });

    $("btn-finish").addEventListener("click", async () => {
      if (mode === "exam") {
        const graded = await grade(questions.map((q) => q.id));
        for (const q of questions) {
          results[q.id] = graded[q.id];
          recordResult(q.topic, q.id, graded[q.id].correct);
        }
      }
      showResult();
    });

    function showResult() {
      const total = questions.length;
      const hits = questions.filter((q) => results[q.id]?.correct).length;
      const pct = Math.round((hits / total) * 100);
      $("result-title").textContent = `${hits} de ${total} corretas (${pct}%)`;
      $("result-summary").textContent =
        pct >= 70 ? "Bom desempenho! Continue revisando os pontos errados." : "Revise os tópicos abaixo e tente novamente.";

      const byTopic = {};
      for (const q of questions) {
        byTopic[q.topic] = byTopic[q.topic] || { total: 0, hits: 0 };
        byTopic[q.topic].total += 1;
        if (results[q.id]?.correct) byTopic[q.topic].hits += 1;
      }
      $("result-topics").replaceChildren(
        ...Object.entries(byTopic).map(([slug, t]) => {
          const link = el("a", { href: `/topicos/${slug}` }, topicNames[slug] || slug);
          return el("li", {}, [link, ` — ${t.hits}/${t.total}`]);
        })
      );

      $("result-review").replaceChildren(
        ...questions.map((q) => {
          const r = results[q.id];
          const picked = selections[q.id] || [];
          const text = (list) => (list.length ? list.map((i) => q.options[i]).join(" · ") : "(sem resposta)");
          const item = el("li", { className: r?.correct ? "ok" : "bad" }, [
            el("strong", {}, `${r?.correct ? "✓" : "✗"} ${q.text}`),
            el("div", {}, `Sua resposta: ${text(picked)}`),
          ]);
          if (!r?.correct) item.append(el("div", {}, `Resposta correta: ${text(r.answer)}`));
          item.append(el("div", { className: "muted" }, r.explanation));
          return item;
        })
      );
      show(resultBox);
    }

    $("btn-restart").addEventListener("click", () => {
      $("retry-wrong").hidden = loadState().wrong.length === 0;
      show(setup);
    });
  }

  const page = document.body.dataset.page;
  const pages = { index: initIndex, topic: initTopic, flashcards: initFlashcards, quiz: initQuiz };
  if (pages[page]) pages[page]();
})();
