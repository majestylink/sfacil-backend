import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CustomerComponent } from './customer/customer.component';
import { CustomerService } from './customer.service';
import { HttpClientModule } from '@angular/common/http';
import { PurchasesComponent } from './purchases/purchases.component';

@NgModule({
  declarations: [
    AppComponent,
    CustomerComponent,
    PurchasesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [CustomerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
