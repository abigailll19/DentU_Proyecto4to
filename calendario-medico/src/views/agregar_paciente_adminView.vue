<template>
  <div class="container">
    <!-- Calendario Principal -->
    <div id="calendar" class="card">
      <div class="header">
        <div>2025</div>
        <div id="monthYear">Mayo 2025</div>
      </div>
      <div class="nav-month">
        <button @click="previousMonth">◀</button>
        <h2 style="margin:0; font-size:18px;" id="monthYearNav">Julio 2025</h2>
        <button @click="nextMonth">▶</button>
      </div>
      <div class="weekdays">
        <div>L</div><div>M</div><div>M</div><div>J</div><div>V</div><div>S</div><div>D</div>
      </div>
      <div id="calendar-grid"></div>
    </div>

    <!-- Panel de pacientes del día -->
    <div id="patients-panel" class="card">
      <div class="header">
        <span id="selected-date">Jueves 4 de Mayo</span>
      </div>
      <h3 style="margin:0 0 15px 0; font-size:16px;">Pacientes agendados</h3>
      <div id="patients-list"></div>

      <button id="add-patient-btn">Agregar Paciente</button>

      <div id="add-patient-form">
        <h4 style="margin:0 0 10px 0;">Nuevo Paciente</h4>
        <select id="doctor-select">
          <option value="">— Seleccione Doctor —</option>
          <option value="garcia">Dr. García</option>
          <option value="mendoza">Dra. Mendoza</option>
        </select>
        <input type="text"   id="patient-name" placeholder="Nombre del paciente" />
        <input type="time"   id="patient-time" />
        <input type="number" id="patient-age"  placeholder="Edad del paciente" />
        <div class="actions">
          <button id="save-patient-btn">Guardar</button>
          <button id="cancel-patient-btn">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AgregarPaciente',
  mounted() {
    let patientsData = JSON.parse(localStorage.getItem('infopacientes.json')) || {
      '2025-05-01': [ { name: 'María García', time: '09:00', age: '30' }, { name: 'Carlos López', time: '10:30', age: '45' } ],
      '2025-05-02': [ { name: 'Ana Martínez', time: '11:00', age: '' } ]
    };
    let currentMonth = 6;      // Julio
    let currentYear = 2025;
    let selectedDate = null;

    const months   = [ 'Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre' ];
    const dayNames = [ 'Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado' ];

    function getDayStatus(dateStr) {
      const patients = patientsData[dateStr] || [];
      if (patients.length === 0) return 'available';
      if (patients.length >= 3) return 'full';
      return 'partial';
    }
    function getDayColor(status) {
      switch (status) {
        case 'available': return '#90c695';
        case 'partial':   return '#ff9800';
        case 'full':      return '#f44336';
        default:          return '#e0e0e0';
      }
    }
    function generateCalendar() {
      const firstDay = new Date(currentYear, currentMonth, 1);
      const lastDay  = new Date(currentYear, currentMonth + 1, 0);
      const startDow = (firstDay.getDay() + 6) % 7;
      const daysIn   = lastDay.getDate();
      document.getElementById('monthYear').textContent = `${months[currentMonth]} ${currentYear}`;
      const grid = document.getElementById('calendar-grid');
      grid.innerHTML = '';
      for (let i = 0; i < startDow; i++) {
        const e = document.createElement('div');
        e.style.height = '40px';
        grid.appendChild(e);
      }
      for (let d = 1; d <= daysIn; d++) {
        const dateStr = `${currentYear}-${String(currentMonth+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
        const status  = getDayStatus(dateStr);
        const cell    = document.createElement('div');
        cell.textContent = d;
        cell.style.cssText = `
          height:40px;display:flex;align-items:center;justify-content:center;
          background-color:${getDayColor(status)};
          cursor:pointer;border-radius:4px;font-weight:bold;border:2px solid transparent;
        `;
        cell.onclick = () => selectDate(d, dateStr);
        grid.appendChild(cell);
      }
    }

    function selectDate(day, dateStr) {
      selectedDate = dateStr;
      const date = new Date(currentYear, currentMonth, day);
      document.getElementById('selected-date').textContent =
        `${dayNames[date.getDay()]} ${day} de ${months[currentMonth]}`;
      document.getElementById('patients-panel').style.display = 'block';
      updatePatientsList();
    }

    function updatePatientsList() {
      const list = document.getElementById('patients-list');
      list.innerHTML = '';
      const addBtn = document.getElementById('add-patient-btn');
      const arr = patientsData[selectedDate] || [];
      arr.forEach((p, idx) => {
        const div = document.createElement('div');
        div.style.cssText = `
          background:white;border:2px solid #4a5d23;border-radius:20px;
          padding:8px 15px;margin-bottom:8px;display:flex;justify-content:space-between;
          align-items:center;
        `;
        div.innerHTML = `
          <div>
            <div style="font-weight:bold;">${p.name}</div>
            <div style="font-size:12px;color:#666;">${p.time}</div>
          </div>
          <button class="remove-btn" data-idx="${idx}">×</button>
        `;
        list.appendChild(div);
      });
      // deshabilitar/agregar
      if (arr.length >= 3) {
        addBtn.style.backgroundColor = '#f44336';
        addBtn.disabled = true;
      } else {
        addBtn.style.backgroundColor = '#ff9800';
        addBtn.disabled = false;
      }
    }

    function addPatient() {
      if (!selectedDate) {
        alert('Selecciona primero una fecha en el calendario.');
        return;
      }
      const doctor = document.getElementById('doctor-select').value;
      const name   = document.getElementById('patient-name').value.trim();
      const time   = document.getElementById('patient-time').value;
      const age    = document.getElementById('patient-age').value.trim();
      if (!doctor || !name || !time || !age) {
        alert('Completa todos los campos.');
        return;
      }
      if (!patientsData[selectedDate]) patientsData[selectedDate] = [];
      patientsData[selectedDate].push({ doctor, name, time, age });
      patientsData[selectedDate].sort((a,b)=>a.time.localeCompare(b.time));
      localStorage.setItem('infopacientes.json', JSON.stringify(patientsData));
      cancelAddPatient();
      updatePatientsList();
      generateCalendar();
    }

    function removePatient(e) {
      if (!e.target.classList.contains('remove-btn')) return;
      const idx = +e.target.dataset.idx;
      if (!confirm('¿Eliminar este paciente?')) return;
      patientsData[selectedDate].splice(idx,1);
      if (patientsData[selectedDate].length === 0) delete patientsData[selectedDate];
      localStorage.setItem('infopacientes.json', JSON.stringify(patientsData));
      updatePatientsList();
      generateCalendar();
    }

    function showAdd() {
      document.getElementById('add-patient-form').style.display = 'block';
      document.getElementById('add-patient-btn').style.display  = 'none';
    }
    function cancelAddPatient() {
      document.getElementById('add-patient-form').style.display = 'none';
      document.getElementById('add-patient-btn').style.display  = 'block';
      ['patient-name','patient-time','patient-age'].forEach(id=>document.getElementById(id).value='');
    }

    // Generar calendario y listeners
    generateCalendar();
    document.getElementById('add-patient-btn').addEventListener('click', showAdd);
    document.getElementById('save-patient-btn').addEventListener('click', addPatient);
    document.getElementById('cancel-patient-btn').addEventListener('click', cancelAddPatient);
    document.getElementById('patients-list').addEventListener('click', removePatient);
  }
}
</script>


<style scoped src="../styles/agregar_paciente_admin.css"></style>
