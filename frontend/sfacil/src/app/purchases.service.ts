import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Purchase } from './myModels';

@Injectable({
  providedIn: 'root'
})
export class PurchasesService {
  private baseUrl = 'http://localhost:8000/api/'; // Replace with your API URL

  constructor(private http: HttpClient) { }

  getCustomerPurchases(customerId: number): Observable<Purchase[]> {
    return this.http.get<Purchase[]>(`${this.baseUrl}purchases/${customerId}/`);
  }
}
