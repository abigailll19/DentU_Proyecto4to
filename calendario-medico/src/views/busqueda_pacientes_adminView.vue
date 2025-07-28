<template>
  <div>
    <!-- Contenido principal -->
    <div class="main-container">
      <div class="search-section">
        <div class="search-wrapper">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            class="search-input" 
            id="searchInput"
            placeholder="Buscar por cédula, nombre o teléfono..." 
            @input="searchPatients"
            @focus="onFocus"
            @blur="onBlur"
          >
        </div>
      </div>

      <div id="results-container">
        <!-- Resultados de pacientes -->
      </div>

      <div class="no-results" id="no-results" style="display: none;">
        No se encontraron pacientes que coincidan con la búsqueda.
      </div>
    </div>

    <!-- Barra de estado -->
    <div class="status-bar">
    </div>
  </div>
</template>

<script>
export default {
  name: 'BusquedaPacientes',
  mounted() {
    // Base de datos simulada de pacientes con información básica
    const patientsDB = [
        {
            id: 'luisa',
            name: 'Luisa Mendoza',
            age: 34,
        },
        {
            id: 'antonio',
            name: 'Antonio Gómez',
            age: 42,
            
        },
        {
            id: 'maria',
            name: 'María Rodríguez',
            age: 28,
        
        }
    ];

    // Leer y "aplanar" todos los pacientes de localStorage
    function getAllPatients() {
      const datos = localStorage.getItem('infopacientes.json');
      if (!datos) return [];
      
      let porFecha;
      try {
        porFecha = JSON.parse(datos);
      } catch (e) {
        console.error('JSON malformado:', e);
        return [];
      }

      // Aplanar [{fecha: '2025-05-01', pacientes: [...]}, ...] → [{id, name, age, time, fecha}, ...]
      const lista = [];
      Object.entries(porFecha).forEach(([fecha, pacientes]) => {
        pacientes.forEach((p, idx) => {
          lista.push({
            id: `${fecha}-${idx}`,   // id único por fecha+índice
            name: p.name,
            age: p.age,
            time: p.time,
            fecha
          });
        });
      });
      return lista;
    }

    function renderPatientCards(patients) {
      const container = document.getElementById('results-container');
      container.innerHTML = '';      // limpio
      document.getElementById('no-results').style.display = patients.length ? 'none' : 'block';

      patients.forEach(p => {
        const card = document.createElement('div');
        card.className = 'patient-card';
        card.innerHTML = `
          <div class="patient-name">${p.name}</div>
          <button class="info-btn" data-id="${p.id}">Ver Información</button>
          <div class="patient-info" id="info-${p.id}" style="display:none;">
            <div class="info-item"><span class="info-label">Fecha:</span> <span class="info-value">${p.fecha}</span></div>
            <div class="info-item"><span class="info-label">Hora:</span> <span class="info-value">${p.time}</span></div>
            <div class="info-item"><span class="info-label">Edad:</span> <span class="info-value">${p.age} años</span></div>
          </div>
        `;
        container.appendChild(card);

        // Toggle info
        const btn = card.querySelector('.info-btn');
        btn.addEventListener('click', () => {
          const info = document.getElementById(`info-${p.id}`);
          if (info.style.display === 'none') {
            info.style.display = 'block';
            btn.textContent = 'Ocultar Información';
          } else {
            info.style.display = 'none';
            btn.textContent = 'Ver Información';
          }
        });
      });

      // Actualizar barra de estado
      updateStatusBar(patients.length);
    }

    window.searchPatients = function() {
      const term = document.getElementById('searchInput').value.toLowerCase();
      const all = getAllPatients();

      if (!term) {
        renderPatientCards(all);
        return;
      }

      const filtered = all.filter(p =>
        p.name.toLowerCase().includes(term) ||
        p.fecha.includes(term) ||
        p.time.includes(term)
      );
      renderPatientCards(filtered);
    }

    function updateStatusBar(count) {
      const bar = document.querySelector('.status-bar');
      bar.textContent = `Clínica Dental - ${count} paciente${count!==1?'s':''} encontrado${count!==1?'s':''}`;
    }

    renderPatientCards(getAllPatients());
    document.getElementById('searchInput').addEventListener('input', searchPatients);

    window.addEventListener('storage', e => {
      if (e.key === 'infopacientes.json') {
        renderPatientCards(getAllPatients());
      }
    });

    // Función para mostrar u ocultar la información detallada de un paciente
    window.toggleInfo = function(patientId) {
        // Obtener el div que contiene la info del paciente usando su id
        const infoDiv = document.getElementById(`info-${patientId}`);
        // Obtener el botón anterior al div para cambiar su texto y estilo
        const button = infoDiv.previousElementSibling;

        // Si la info está oculta, mostrarla y cambiar texto y color del botón
        if (infoDiv.style.display === 'none' || infoDiv.style.display === '') {
            infoDiv.style.display = 'block';
            button.textContent = 'Ocultar Información';
            button.style.backgroundColor = '#d0d0d0';  // color gris claro
        } else {
            // Si la info está visible, ocultarla y restaurar texto y color del botón
            infoDiv.style.display = 'none';
            button.textContent = 'Ver Información';
            button.style.backgroundColor = '#f0f0f0';  // color gris más claro
        }
    }

    // Función para actualizar la barra de estado con el número de pacientes encontrados
    function updateStatusBar(count) {
        const statusBar = document.querySelector('.status-bar');
        statusBar.textContent = `Clínica Dental - Sistema de Gestión de Pacientes | ${count} paciente${count !== 1 ? 's' : ''} encontrado${count !== 1 ? 's' : ''}`;
    }

    document.getElementById('searchInput').addEventListener('focus', function () {
        this.placeholder = 'Escriba para buscar...';
    });

    document.getElementById('searchInput').addEventListener('blur', function () {
        if (this.value === '') {
            this.placeholder = 'Buscar por cédula, nombre o teléfono...';
        }
    });
  }
}
</script>

<style scoped src="../styles/busqueda_pacientes_admin.css"></style>
