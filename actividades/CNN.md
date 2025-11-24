---
tags:
  - actividad
  - inteligencia-artificial
  - unidad-3
date: 2025-11-02
---
## 1. Valores por defecto
Valores por defecto:
```python
#declaramos variables con los parámetros de configuración de la red
INIT_LR = 1e-3 # Valor inicial de learning rate. El valor 1e-3 corresponde con 0.001
epochs = 20 # Cantidad de iteraciones completas al conjunto de imagenes de entrenamiento
batch_size = 64 # cantidad de imágenes que se toman a la vez en memoria
```
![[Pasted image 20251102233724.png]]
![[Pasted image 20251102233758.png]]

### Evaluaciones
```c
Test loss: 0.08118366450071335
Test accuracy: 0.9795150756835938
```
### Historial
```json
{'accuracy': [0.7702639698982239,
  0.8755494952201843,
  0.8905816078186035,
  0.894511878490448,
  0.9050059914588928,
  0.908429741859436,
  0.9093008637428284,
  0.9127448797225952,
  0.9139401316642761,
  0.9117521643638611,
  0.9180324673652649,
  0.9165332913398743,
  0.9193493127822876,
  0.9218816757202148,
  0.9228743314743042,
  0.9208889603614807,
  0.9240695834159851,
  0.9207268953323364,
  0.9264601469039917,
  0.9237859845161438],
 'loss': [0.6963513493537903,
  0.3964339792728424,
  0.3517572581768036,
  0.3406437039375305,
  0.30777913331985474,
  0.30664145946502686,
  0.307345449924469,
  0.2972869575023651,
  0.296621173620224,
  0.3121330142021179,
  0.2890572249889374,
  0.3039090037345886,
  0.2947597801685333,
  0.293508380651474,
  0.28223198652267456,
  0.29147768020629883,
  0.2857797145843506,
  0.30889251828193665,
  0.27729532122612,
  0.29956451058387756],
 'val_accuracy': [0.932582437992096,
  0.9602138996124268,
  0.9567295908927917,
  0.9553520679473877,
  0.9702617526054382,
  0.9628068804740906,
  0.9708289504051208,
  0.9733408689498901,
  0.9692893624305725,
  0.9692083597183228,
  0.9768252372741699,
  0.9713961482048035,
  0.9769873023033142,
  0.9581881761550903,
  0.9810388088226318,
  0.9775545001029968,
  0.9540556073188782,
  0.9745563864707947,
  0.9689652323722839,
  0.9786078929901123],
 'val_loss': [0.24163630604743958,
  0.12363050132989883,
  0.14205674827098846,
  0.13099956512451172,
  0.09274882823228836,
  0.10986478626728058,
  0.09712078422307968,
  0.08261407166719437,
  0.09507696330547333,
  0.09310771524906158,
  0.07698199898004532,
  0.08667735010385513,
  0.07994546741247177,
  0.10175523161888123,
  0.0653151422739029,
  0.0644908919930458,
  0.11275933682918549,
  0.08057276904582977,
  0.10443567484617233,
  0.08211027830839157]}
```

### Accuracy
![[Pasted image 20251102234433.png]]

### Precisión por clase
```c
              precision    recall  f1-score   support

     Class 0       0.93      0.94      0.94      1884
     Class 1       1.00      0.95      0.97      1806
     Class 2       0.97      0.99      0.98      1532
     Class 3       1.00      0.99      0.99      1470
     Class 4       1.00      1.00      1.00      1465
     Class 5       0.99      0.96      0.97      1028
     Class 6       0.99      0.99      0.99      1518
     Class 7       0.94      0.99      0.96      1916
     Class 8       1.00      1.00      1.00      1053
     Class 9       1.00      1.00      1.00      1754

    accuracy                           0.98     15426
   macro avg       0.98      0.98      0.98     15426
weighted avg       0.98      0.98      0.98     15426
```

### Prediccion
```c
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 40ms/step
./contenido/IA/sportimages/golf/golf_0113.jpg golf
./contenido/IA/sportimages/boxeo/boxeo_0003.jpg boxeo
./contenido/IA/sportimages/ciclismo/ciclismo_0003.jpg ciclismo
./contenido/IA/sportimages/golf/golf_0113.jpg golf
./contenido/IA/sportimages/boxeo/boxeo_0003.jpg boxeo
./contenido/IA/sportimages/f1/f1_0013.jpg f1
./contenido/IA/sportimages/golf/golf_0113.jpg golf
./contenido/IA/sportimages/boxeo/boxeo_0003.jpg boxeo
./contenido/IA/sportimages/ciclismo/ciclismo_0003.jpg ciclismo
./contenido/IA/sportimages/golf/golf_0113.jpg golf
./contenido/IA/sportimages/boxeo/boxeo_0003.jpg boxeo
./contenido/IA/sportimages/ciclismo/ciclismo_0003.jpg ciclismo
./contenido/IA/sportimages/golf/golf_0113.jpg golf
./contenido/IA/sportimages/boxeo/boxeo_0003.jpg boxeo
./contenido/IA/sportimages/ciclismo/ciclismo_0003.jpg ciclismo
```

