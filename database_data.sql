INSERT INTO practica2.CLIENTE (cedula, nombre, apellido, password, telefono) VALUES ('0101130862', 'Kevin', 'Cordero', '123321', 'NA');
INSERT INTO practica2.CLIENTE (cedula, nombre, apellido, password, telefono) VALUES ('0101240612', 'Kevin', 'Godoy', '123321', 'Na x2');
INSERT INTO practica2.CLIENTE (cedula, nombre, apellido, password, telefono) VALUES ('0105652747', 'Leo', 'Alvarado', '123321', '072897510');

INSERT INTO practica2.INSTITUCION_FINANCIERA (id, nombre, direccion, telefono) VALUES (0, 'JEP', 'Parque Industrial', '001002003');
INSERT INTO practica2.INSTITUCION_FINANCIERA (id, nombre, direccion, telefono) VALUES (1, 'BANCO PICHINCHA', 'Frente a la tienda del godoy', '001002003');
INSERT INTO practica2.INSTITUCION_FINANCIERA (id, nombre, direccion, telefono) VALUES (2, 'BANCO DEL AUSTRO', 'Parque Calderon', '001002003');

INSERT INTO practica2.CUENTA_FINANCIERA (id, cliente_cedula, institucion_id, numero_cuenta, saldo_actual) VALUES (0, '0105652747', 0, '001001002', 120);
INSERT INTO practica2.CUENTA_FINANCIERA (id, cliente_cedula, institucion_id, numero_cuenta, saldo_actual) VALUES (1, '0101130862', 1, '002003004', 40);
INSERT INTO practica2.CUENTA_FINANCIERA (id, cliente_cedula, institucion_id, numero_cuenta, saldo_actual) VALUES (2, '0101240612', 2, '003004005', 250);

INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (1, 0, 1, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (2, 0, 1, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (3, 1, 2, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (4, 1, 2, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (5, 1, 2, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (6, 1, 2, 50, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (7, 0, 1, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (8, 0, 1, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (9, 0, 1, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (10, 0, 2, 10, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (11, 2, 0, 30, 'Pago de HBO');
INSERT INTO practica2.TRANSFERENCIA_BANCARIA (id, cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo) VALUES (12, 2, 0, 30, 'Pago de HBO');