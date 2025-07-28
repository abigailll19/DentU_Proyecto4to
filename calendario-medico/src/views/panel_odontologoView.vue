<!-- src/views/PanelOdontologoView.vue -->
<template>
  <div class="browser-frame">
    <div class="content">
      <div class="doctor-header">
        <div class="doctor-name">Dr. {{ doctorId }}</div>
        <div class="date">{{ currentDate }}</div>
      </div>

      <h2 class="section-title">Lista de Pacientes</h2>
      <div class="patient-list" id="patientList">
        <div
          v-if="pacientes.length === 0"
          class="empty-message"
        >
          No tienes pacientes agendados.
        </div>
        <div
          v-for="(pac, idx) in pacientes"
          :key="idx"
          class="patient-card"
          @click="flashCard($event)"
        >
          <div class="patient-icon">👤</div>
          <div class="patient-info">
            <div class="patient-name">{{ pac.name || '—' }}</div>
            <div class="patient-details">
              Edad: {{ pac.age || '?' }} años
              <span class="time">Hora: {{ pac.time || '—' }}</span>
            </div>
          </div>
          <button class="ver-btn" @click.stop="verOdontograma(pac.name)">
            Ver
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PanelOdontologo',
  data() {
    return {
      doctorId: '',
      currentDate: '',
      pacientes: [],
      citas: []
    }
  },
  methods: {
    getCitasData() {
      const raw = localStorage.getItem('citas_paciente');
      return raw ? JSON.parse(raw) : { appointments: [] };
    },

    renderMisCitas() {
      const citasData = this.getCitasData();
      this.citas = citasData.appointments
        .filter(cita => cita.doctor === this.doctorId);
    },

    cargarPacientes() {
      // Leer el JSON completo (objeto con fechas como claves)
      const raw = localStorage.getItem('infopacientes.json') || '{}';
      let porFecha;
      try {
        porFecha = JSON.parse(raw);
      } catch (e) {
        console.error('JSON malformado en infopacientes.json:', e);
        return;
      }

      // Reset del array de pacientes
      this.pacientes = [];

      // Para cada fecha, filtrar solo los pacientes de este doctor
      for (const fecha in porFecha) {
        const pacientesDeLaFecha = porFecha[fecha]
          .filter(pac => pac.doctor === this.doctorId);

        // Agregar los pacientes filtrados al array
        pacientesDeLaFecha.forEach(pac => {
          this.pacientes.push({
            ...pac,
            fecha: fecha
          });
        });
      }
    },

    verOdontograma(nombrePaciente) {
      localStorage.setItem('pacienteActual', nombrePaciente);
      this.$router.push('/odontograma');
    },

    flashCard(event) {
      if (!event.target.classList.contains('ver-btn')) {
        const card = event.currentTarget;
        card.style.backgroundColor = '#f8f9fa';
        setTimeout(() => card.style.backgroundColor = 'white', 150);
      }
    }
  },

  mounted() {
    // Obtener datos del usuario actual
    const usuario = localStorage.getItem('usuarioActual');
    const rol = localStorage.getItem('rol');
    this.doctorId = usuario || null;

    // Protección de acceso
    if (!this.doctorId || rol !== 'odontologo') {
      console.log("Acceso no autorizado. Redirigiendo a login...");
      this.$router.push('/login');
      return;
    }

    // Obtener fecha actual
    const today = new Date();
    const options = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };
    this.currentDate = today.toLocaleDateString('es-ES', options);

    console.log('=== PANEL ODONTÓLOGO ===');
    console.log('Doctor logueado:', this.doctorId);

    // Cargar datos iniciales
    this.cargarPacientes();
    this.renderMisCitas();

    // Escuchar cambios en localStorage
    window.addEventListener('storage', (e) => {
      if (e.key === 'infopacientes.json') {
        this.cargarPacientes();
      }
      if (e.key === 'citas_paciente') {
        this.renderMisCitas();
      }
    });
  },

  beforeUnmount() {
    // Limpiar event listeners
    window.removeEventListener('storage', this.cargarPacientes);
    window.removeEventListener('storage', this.renderMisCitas);
  }
}
</script>


<style scoped src="../styles/panel_odontologo.css"></style>

