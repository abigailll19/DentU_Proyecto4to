<template>
    <div class="odontograma-section">
      <div class="odontograma-title">Odontograma</div>
      
      <div class="controls">
        <button 
          v-for="state in states" 
          :key="state.key"
          class="control-btn" 
          :class="{ active: currentTool === state.key }"
          :data-state="state.key"
          @click="selectTool(state)"
        >
          {{ state.label }}
        </button>
      </div>

      <div class="tooth-info">
        <strong v-if="!toolSelected">1. Selecciona un estado arriba</strong>
        <strong v-else>Estado seleccionado: {{ selectedStateLabel }}</strong><br>
        <strong v-if="!toolSelected">2. Haz clic en cualquier diente para aplicar el estado</strong>
        <strong v-else>Ahora haz clic en cualquier diente para aplicar este estado</strong>
      </div>

      <div class="teeth-grid" id="upperTeeth">
        <div 
          v-for="num in upperNumbers" 
          :key="num"
          class="tooth"
          :class="teethState[num] || 'sano'"
          :data-number="num"
          @click="changeToothState(num)"
        >
          {{ num }}
        </div>
      </div>

      <div class="teeth-grid" id="lowerTeeth">
        <div 
          v-for="num in lowerNumbers" 
          :key="num"
          class="tooth"
          :class="teethState[num] || 'sano'"
          :data-number="num"
          @click="changeToothState(num)"
        >
          {{ num }}
        </div>
      </div>

      <div class="legend">
        <div class="legend-item">
          <div class="legend-color sano"></div><span>Sano</span>
        </div>
        <div class="legend-item">
          <div class="legend-color caries"></div><span>Caries</span>
        </div>
        <div class="legend-item">
          <div class="legend-color arreglado"></div><span>Arreglado</span>
        </div>
        <div class="legend-item">
          <div class="legend-color faltante"></div><span>Faltante</span>
        </div>
      </div>
    </div>

    <div class="notes-section">
      <div class="notes-title">Notas del tratamiento</div>
      <textarea 
        class="notes-textarea" 
        v-model="treatmentNotes"
        placeholder="Ingrese las notas del tratamiento aquí..."
      ></textarea>
    </div>

    <button class="save-btn" @click="saveChanges">📁 Guardar cambios</button>

    <div class="history-section">
      <div class="history-title">Historial reciente</div>
      <div id="historyList">
        <div 
          v-for="entry in displayedHistory" 
          :key="entry"
          class="history-item"
          style="border-left-color: #27ae60;"
        >
          {{ entry }}
        </div>
      </div>
    </div>
</template>


<script>
export default {
  name: 'Odontograma',
  data() {
    return {
      currentTool: null,
      treatmentNotes: '',
      teethState: {},
      historyEntries: [],
      states: [
        { key: 'sano', label: 'Sano' },
        { key: 'caries', label: 'Caries' },
        { key: 'arreglado', label: 'Arreglado' },
        { key: 'faltante', label: 'Faltante' }
      ],
      upperNumbers: [18,17,16,15,14,13,12,11,21,22,23,24,25,26,27,28],
      lowerNumbers: [48,47,46,45,44,43,42,41,31,32,33,34,35,36,37,38]
    };
  },
  computed: {
    toolSelected() {
      return !!this.currentTool;
    },
    selectedStateLabel() {
      const state = this.states.find(s => s.key === this.currentTool);
      return state ? state.label : '';
    },
    displayedHistory() {
      return this.historyEntries.slice(0, 5);
    }
  },
  mounted() {
    this.loadSavedState();
  },
  methods: {
    selectTool(state) {
      this.currentTool = state.key;
    },
    changeToothState(number) {
      if (!this.currentTool) return;

      const oldState = this.teethState[number] || 'sano';
      this.teethState[number] = this.currentTool;

      if (oldState !== this.currentTool) {
        this.addToHistory(`Diente ${number}: ${oldState} → ${this.currentTool}`);
      }

      this.saveToLocalStorage();
    },
    addToHistory(entry) {
      const now = new Date();
      const dateStr = now.toLocaleDateString('es-ES');
      const timeStr = now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
      const fullEntry = `${dateStr} ${timeStr} - ${entry}`;
      this.historyEntries.unshift(fullEntry);
    },
    saveToLocalStorage() {
      const data = {
        teethState: this.teethState,
        historyEntries: this.historyEntries,
        notes: this.treatmentNotes,
        lastModified: new Date().toISOString()
      };
      localStorage.setItem('info_odontograma', JSON.stringify(data));
    },
    loadSavedState() {
      try {
        const saved = JSON.parse(localStorage.getItem('info_odontograma'));
        if (saved) {
          this.teethState = saved.teethState || {};
          this.historyEntries = saved.historyEntries || [];
          this.treatmentNotes = saved.notes || '';
        }
      } catch (err) {
        console.error('Error cargando datos:', err);
      }
    },
    saveChanges() {
      this.saveToLocalStorage();
      if (this.treatmentNotes.trim()) {
        this.addToHistory(`Notas actualizadas: ${this.treatmentNotes.slice(0, 30)}${this.treatmentNotes.length > 30 ? '...' : ''}`);
        this.saveToLocalStorage();
      }
      alert('¡Cambios guardados!');
    }
  }
};
</script>




<style scoped src="../styles/odontograma.css"></style>
