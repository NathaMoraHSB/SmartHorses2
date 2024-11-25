import {
  ChangeDetectorRef,
  Component,
  Input,
  Output,
  EventEmitter,
  OnChanges,
  OnInit,
  OnDestroy,
  SimpleChanges,
  TemplateRef,
  ViewChild
} from '@angular/core';
import { MatCard, MatCardContent, MatCardHeader, MatCardModule } from "@angular/material/card";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatSelectModule } from "@angular/material/select";
import { MatRadioModule } from "@angular/material/radio";
import { MatButtonModule } from "@angular/material/button";
import { FormsModule } from "@angular/forms";
import { CommonModule, NgIf, NgClass } from "@angular/common";
import { HttpClientModule } from "@angular/common/http";
import { ServicesService } from "../services.service";
import {MatDialog, MatDialogModule} from '@angular/material/dialog';

@Component({
  selector: 'app-complete',
  standalone: true,
  imports: [
    MatCard, MatCardContent, MatCardHeader, MatCardModule,
    MatFormFieldModule, MatSelectModule, MatRadioModule,
    MatButtonModule, FormsModule, NgIf, NgClass,
    CommonModule, HttpClientModule, MatDialogModule
  ],
  templateUrl: './complete.component.html',
  styleUrls: ['./complete.component.css']
})
export class CompleteComponent implements OnInit {
  @ViewChild('experimentResultsTemplate') experimentResultsTemplate!: TemplateRef<any>;
  grid: number[][] = [];
  turno_humano: boolean = true;
  whiteHorsePoints: number = 0;
  blackHorsePoints: number = 0;
  quedan_puntos: boolean = true;
  dos_x_blanco: boolean = false;
  dos_x_negro: boolean= false;

  juego_en_curso: boolean = false;
  humanVSmachine: boolean = false;
  isExperiment: boolean= false;
  difficultyLevel: number = 2;
  simulationInterval: any;

  possibleMoves: [number, number][] = [];
  highlightCells: Set<string> = new Set();

  constructor(
    private matrixService: ServicesService,
    private cdr: ChangeDetectorRef,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.startMatrix();
  }

  startMatrix(): void {
    this.matrixService.startMatrix().subscribe(
      response => {
        if (response && response.matrix) {
          this.grid = response.matrix;
        } else {
          console.error('No matrix received');
        }
      },
      error => {
        console.error('Error loading matrix:', error);
      }
    );
  }

  startSimulation(): void {
    if(this.isExperiment){
      this.openExperimentDialog();
    }else{
      this.juego_en_curso = true;
      this.set_dificulty();
      if (!this.humanVSmachine) {
        this.runIaVsIaSimulation();
      } else {
        this.runIaVsHumanSimulation();
        this.humanVSmachine=true
      }
    }

  }

  runIaVsIaSimulation(): void {
    console.log("Running IA vs IA simulation...");
    this.matrixService.startSimulation().subscribe(
      response => {
        if (response && response.simulation && response.report) {
          const simulation = response.simulation;
          const report = response.report;
          let index = 0;

          if (this.simulationInterval) {
            clearInterval(this.simulationInterval);
          }

          this.simulationInterval = setInterval(() => {
            if (index < simulation.length) {
              const turn = simulation[index];
              this.grid = turn.matrix;
              this.whiteHorsePoints = turn.whiteHorsePoints;
              this.blackHorsePoints = turn.blackHorsePoints;
              this.dos_x_blanco = turn.whiteHorseMultiplier;
              this.dos_x_negro = turn.blackHorseMultiplier;
              index++;
            } else {
              clearInterval(this.simulationInterval);
              console.log("Simulation complete.");
              this.quedan_puntos = false;
              console.log("Final Report:", report);
            }
          }, 1000);
        } else {
          console.error("Simulation data or report not received");
        }
      },
      error => {
        console.error("Error during simulation:", error);
      }
    );
  }

  runIaVsHumanSimulation(): void {
    const playTurn = () => {
      this.checkIfGameContinues(() => {
        if (this.quedan_puntos) {
          console.log("Turno de la máquina.");
          this.machineTurn(() => {
           this.checkIfGameContinues(() => {
              if (this.quedan_puntos) {
                console.log("Turno del humano.");
                this.activateHumanTurn();
              } else {
                console.log("El juego ha terminado.");
              }
            });
          });
        } else {
          console.log("El juego ha terminado.");
        }
      });
    };
    playTurn();
  }

  machineTurn(callback?: () => void): void {
    console.log("Turno de la máquina...");
    this.matrixService.getIaMove().subscribe(
      response => {
        if (response.simulation) {
          this.processSimulation(response.simulation);
          if (callback) callback();
        } else {
          console.error("No se recibió la simulación desde el backend.");
        }
      },
      error => console.error("Error al solicitar movimiento de la máquina:", error)
    );
  }

  activateHumanTurn(): void {
    setTimeout(() => {
      this.turno_humano = true;
      this.highlightPossibleMoves();
    }, 3000);
  }

  checkIfGameContinues(callback: () => void): void {
    this.matrixService.checkQuedanPuntos().subscribe(response => {
      this.quedan_puntos = response.quedan_puntos;
      console.log(`Quedan puntos: ${this.quedan_puntos}`);
      if (callback) callback();
    });
  }

  onCellClick(row: number, col: number): void {
    if (this.turno_humano && this.highlightCells.has(`${row},${col}`)) {
      console.log("Movimiento humano recibido:", { row, col });

      this.updateBlackHorsePosition(row, col);

      this.clearHighlightedCells();

      this.turno_humano = false;

      this.sendMoveToBackend({ selectedCell: { row, col } });
    } else {
      console.warn("Movimiento inválido o no es el turno del humano.");
    }
  }

  updateBlackHorsePosition(row: number, col: number): void {
    for (let i = 0; i < this.grid.length; i++) {
      for (let j = 0; j < this.grid[i].length; j++) {
        if (this.grid[i][j] === 12) {
          this.grid[i][j] = 0;
        }
      }
    }

    this.grid[row][col] = 12;
    console.log("Nueva posición del caballo negro actualizada en la matriz.");
  }

  sendMoveToBackend(data: { selectedCell: { row: number; col: number } }): void {
    this.matrixService.sendHumanMove(data).subscribe(
      response => {
        this.turno_humano = false;
        if (response.simulation) {
          this.processSimulation(response.simulation);
          this.runIaVsHumanSimulation();
        }
      },
      error => {
        console.error("Error al enviar coordenadas al backend:", error);
      }
    );
  }

  processSimulation(simulation: any[]): void {
    let index = 0;
    if (this.simulationInterval) {
      clearInterval(this.simulationInterval);
    }
    this.simulationInterval = setInterval(() => {
      if (index < simulation.length) {
        const turn = simulation[index];
        this.grid = turn.matrix;
        this.whiteHorsePoints = turn.whiteHorsePoints;
        this.blackHorsePoints = turn.blackHorsePoints;
        this.dos_x_blanco = turn.whiteHorseMultiplier;
        this.dos_x_negro = turn.blackHorseMultiplier;
        index++;
      } else {
        clearInterval(this.simulationInterval);
      }
    }, 1000);
  }

  set_dificulty(): void {
    this.matrixService.updateDifficulty(this.difficultyLevel).subscribe(
      response => console.log("Dificultad actualizada:", response),
      error => {
        console.error("Error al actualizar la dificultad:", error);
        this.juego_en_curso = false;
      }
    );
  }

  highlightPossibleMoves(): void {
    if (!this.turno_humano) return;
    const { x, y } = this.getBlackHorsePosition();
    this.possibleMoves = this.movimientosPosibles(x, y, this.grid.length);
    this.highlightCells.clear();
    this.possibleMoves.forEach(([row, col]) => {
      this.highlightCells.add(`${row},${col}`);
    });
    this.cdr.detectChanges();
    console.log("Celdas destacadas:", this.highlightCells);
  }

  clearHighlightedCells(): void {
    this.highlightCells.clear();
    this.cdr.detectChanges();
  }

  movimientosPosibles(x: number, y: number, n: number): [number, number][] {
    const movimientos = [
      [2, 1], [2, -1], [-2, 1], [-2, -1],
      [1, 2], [1, -2], [-1, 2], [-1, -2]
    ];
    const movimientosValidos: [number, number][] = [];

    movimientos.forEach(([dx, dy]) => {
      const nx = x + dx;
      const ny = y + dy;
      if (0 <= nx && nx < n && 0 <= ny && ny < n && this.grid[nx][ny] !== 11 && this.grid[nx][ny] !== 12) {
        movimientosValidos.push([nx, ny]);
      }
    });
    return movimientosValidos;
  }

  getBlackHorsePosition(): { x: number; y: number } {
    for (let i = 0; i < this.grid.length; i++) {
      for (let j = 0; j < this.grid[i].length; j++) {
        if (this.grid[i][j] === 12) {
          return { x: i, y: j };
        }
      }
    }
    return { x: -1, y: -1 };
  }

  resetGame(){
    this.whiteHorsePoints=0;
    this.blackHorsePoints =0;
    this.quedan_puntos= true;
    this.dos_x_blanco = false;
    this.dos_x_negro= false;
    this.startMatrix();
    this.juego_en_curso= false;
    this.turno_humano= false;
    this.isExperiment = false;
  }

  openExperimentDialog(): void {
    this.matrixService.getExperimentResults().subscribe((response: any) => {
      const processedData = this.prepareExperimentData(response);

      const dialogRef = this.dialog.open(this.experimentResultsTemplate, {
        width: '600px',
        data: processedData,
      });

      dialogRef.afterClosed().subscribe(() => {
        console.log('El diálogo fue cerrado.');
        this.resetGame(); // Reinicia el juego
      });
    });
  }


  prepareExperimentData(data: any): { rows: any[], totals: any } {
    const rows: { ai1: string; values: string[] }[] = []; // Define 'values' como un array de strings
    const totals = data.totals;

    const difficultyLevels: string[] = ['Principiante', 'Amateur', 'Experto'];

    for (const ai1Level of difficultyLevels) {
      const row: { ai1: string; values: string[] } = { ai1: ai1Level, values: [] }; // Especifica el tipo explícito
      for (const ai2Level of difficultyLevels) {
        const result = data.details[ai1Level][ai2Level];
        row.values.push(`${result.wins_ai1}-${result.wins_ai2}-${result.draws}`);
      }
      rows.push(row);
    }

    return { rows, totals };
  }




}
