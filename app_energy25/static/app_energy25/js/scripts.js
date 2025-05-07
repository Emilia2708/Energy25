/**
 * scripts.js
 *
 * Plik zawierający kod JavaScript dla strony Energy25.
 */

// Poniżej znajdują się przykładowe funkcje, które można dodać do tego pliku.
// Pamiętaj, aby dostosować je do konkretnych potrzeb Twojej strony.

/**
 * Funkcja do obsługi kliknięcia przycisku "Pokaż więcej" dla lokalizacji elektrowni.
 */
function pokazWiecejLokalizacji(typElektrowni) {
  const listaLokalizacji = document.querySelector(
    .lokalizacje-${typElektrowni}
  );
  if (listaLokalizacji.style.maxHeight === "200px") {
    listaLokalizacji.style.maxHeight = "none";
    listaLokalizacji.style.overflow = "visible";
    // Zmień tekst przycisku na "Zwiń"
    const przycisk = document.querySelector(
      .pokaz-wiecej-${typElektrowni}
    );
    if (przycisk) {
      przycisk.textContent = "Zwiń";
    }
  } else {
    listaLokalizacji.style.maxHeight = "200px";
    listaLokalizacji.style.overflow = "hidden";
    // Zmień tekst przycisku na "Pokaż więcej"
    const przycisk = document.querySelector(
      .pokaz-wiecej-${typElektrowni}
    );
    if (przycisk) {
      przycisk.textContent = "Pokaż więcej";
    }
  }
}

/**
 * Funkcja do animacji licznika energii.
 */
function animujLicznikEnergii(elementId, koncowaWartosc, czasTrwania = 2000) {
  const element = document.getElementById(elementId);
  if (!element) return;

  let poczatkowaWartosc = 0;
  const roznica = koncowaWartosc - poczatkowaWartosc;
  let startTimestamp = null;

  function krok(timestamp) {
    if (!startTimestamp) startTimestamp = timestamp;
    const postep = timestamp - startTimestamp;
    const procent = Math.min(postep / czasTrwania, 1);
    element.textContent = Math.floor(poczatkowaWartosc + roznica * procent);
    if (procent < 1) {
      window.requestAnimationFrame(krok);
    } else {
      element.textContent = koncowaWartosc; // Upewnij się, że wyświetlana jest dokładna wartość końcowa
    }
  }

  window.requestAnimationFrame(krok);
}

// Przykładowe użycie funkcji animujLicznikEnergii:
// Po załadowaniu strony, rozpocznij animację dla licznika o id "energia-wiatrowa" do wartości 15000 MWh w ciągu 2 sekund.
document.addEventListener("DOMContentLoaded", () => {
  animujLicznikEnergii("energia-wiatrowa", 15000, 2000);
});

/**
 * Funkcja do dynamicznego wykresu produkcji energii.
 * (Wymaga biblioteki Chart.js)
 */
function renderWykresProdukcjiEnergii(
  canvasId,
  tytul,
  daneRoczne,
  jednostka = "MWh"
) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(daneRoczne),
      datasets: [
        {
          label: tytul,
          data: Object.values(daneRoczne),
          backgroundColor: [
            "rgba(54, 162, 235, 0.6)",
            "rgba(255, 206, 86, 0.6)",
            "rgba(75, 192, 192, 0.6)",
            "rgba(153, 102, 255, 0.6)",
            "rgba(255, 159, 64, 0.6)",
          ],
          borderColor: [
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: tytul,
          font: {
            size: 16,
          },
        },
        legend: {
          position: "bottom",
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return value + " " + jednostka; // Dodaj jednostkę do osi Y
            },
          },
        },
      },
    },
  });
}

// Przykładowe dane i użycie funkcji renderWykresProdukcjiEnergii:
// Załóżmy, że mamy dane produkcji energii wiatrowej i fotowoltaicznej za kilka lat.
const daneProdukcjiWiatrowej = {
  2020: 10000,
  2021: 12000,
  2022: 15000,
  2023: 18000,
  2024: 20000,
};

const daneProdukcjiFotowoltaicznej = {
  2020: 5000,
  2021: 7000,
  2022: 9000,
  2023: 11000,
  2024: 13000,
};

document.addEventListener("DOMContentLoaded", () => {
  renderWykresProdukcjiEnergii(
    "wykres-wiatrowy",
    "Produkcja Energii Elektrycznej z Elektrowni Wiatrowej",
    daneProdukcjiWiatrowej,
    "MWh"
  );
  renderWykresProdukcjiEnergii(
    "wykres-fotowoltaiczny",
    "Produkcja Energii Elektrycznej z Elektrowni Fotowoltaicznej",
    daneProdukcjiFotowoltaicznej,
  "MWh"
  );
});