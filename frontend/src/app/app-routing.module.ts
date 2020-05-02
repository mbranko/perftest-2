import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home';
import { LoginComponent } from './components/login';
import { StartTestComponent } from './components/start-test';
import { PitanjeComponent } from './components/pitanje';
import { EndTestComponent } from './components/end-test';

const routes: Routes = [{
    path: '',
    component: HomeComponent,
  }, {
    path: 'test/:id',
    component: StartTestComponent,
  }, {
    path: 'pitanje/:rbr',
    component: PitanjeComponent,
  }, {
    path: 'finish',
    component: EndTestComponent,
  }, {
    path: 'login',
    component: LoginComponent,
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
