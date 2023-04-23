import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CustomerComponent } from './customer/customer.component';
import { PurchasesComponent } from './purchases/purchases.component';

const routes: Routes = [
  { path: 'customers', component: CustomerComponent },
  { path: 'purchases/:customerId', component: PurchasesComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
