import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { GeolocationContainerComponent } from './containers/geolocation-container/geolocation-container.component';

const routes: Routes = [
  { path: '', component: AppComponent },
  { path: 'geolocation', component: GeolocationContainerComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
