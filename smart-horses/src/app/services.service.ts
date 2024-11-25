import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {catchError, Observable, throwError} from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ServicesService {
  private baseUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) { }

  startMatrix(): Observable<any> {
    console.log('Starting simulation...');
    return this.http.post<any>(`${this.baseUrl}/start`, {}).pipe(
      tap(response => console.log('Simulation started, initial matrix:', response))
    );
  }

  startSimulation(): Observable<any> {
    console.log('Starting simulation...');
    return this.http.post<any>(`${this.baseUrl}/partidaIaVSIa`, {}).pipe(
      tap(response => console.log('Simulation started, response:', response)),
      catchError(this.handleError)  // Manejo de errores
    );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // Error del lado del cliente o red
      console.error('An error occurred:', error.error.message);
    } else {
      // Error del lado del servidor
      console.error(`Backend returned code ${error.status}, body was: ${error.error}`);
    }
    return throwError('Something bad happened; please try again later.');
  }

  sendHumanMove(data: any): Observable<any> {
    console.log('Enviando movimiento del humano al backend...', data);
    const formattedData = {
      row: data.selectedCell.row,
      col: data.selectedCell.col
    };

    console.log('Enviando movimiento del humano al backend...', formattedData);
    return this.http.post<any>(`${this.baseUrl}/human-move`, formattedData).pipe(
      tap(response => console.log('Movimiento enviado, respuesta del backend:', response)),
      catchError(this.handleError)
    );
  }


  updateDifficulty(difficulty: number): Observable<any> {
    console.log(`Actualizando dificultad a: ${difficulty}`);
    return this.http.post<any>(`${this.baseUrl}/update-difficulty`, { difficulty }).pipe(
      tap(response => console.log('Dificultad actualizada:', response)),
      catchError(this.handleError)
    );
  }

  getIaMove(): Observable<any> {
    console.log('Solicitando movimiento de la IA al backend...');
    return this.http.get<any>(`${this.baseUrl}/ai-turn`).pipe(
      tap(response => console.log('Movimiento de la IA recibido:', response)),
      catchError(this.handleError)
    );
  }

  checkQuedanPuntos(): Observable<{ quedan_puntos: boolean }> {
    console.log('Verificando si quedan puntos en el tablero...');
    return this.http.get<{ quedan_puntos: boolean }>(`${this.baseUrl}/quedan-puntos`).pipe(
      tap(response => {
        if (response.quedan_puntos) {
          console.log('Todavía quedan puntos en el tablero.');
        } else {
          console.log('No quedan puntos en el tablero. El juego ha terminado.');
        }
      }),
      catchError(this.handleError) // Manejo de errores
    );
  }

  getExperimentResults(): Observable<any> {
    console.log('Obteniendo resultados de los experimentos...');
    return this.http.get<any>(`${this.baseUrl}/run-experiments`).pipe(
      tap(response => console.log('Resultados de los experimentos recibidos:', response)),
      catchError(this.handleError)
    );
  }

}
