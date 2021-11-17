create table CLIENTE
(
    cedula   varchar(10)  not null
        primary key,
    nombre   varchar(255) null,
    apellido varchar(255) null,
    password varchar(255) null,
    telefono varchar(255) null
);

create table INSTITUCION_FINANCIERA
(
    id        int(10)      not null
        primary key,
    nombre    varchar(255) null,
    direccion varchar(255) null,
    telefono  varchar(255) null
);

create table CUENTA_FINANCIERA
(
    id             bigint        not null
        primary key,
    cliente_cedula varchar(10)   null,
    institucion_id int(10)       null,
    numero_cuenta  varchar(255)  null,
    saldo_actual   double(12, 4) null,
    constraint CUENTA_FINANCIERA_CLIENTE_cedula_fk
        foreign key (cliente_cedula) references CLIENTE (cedula),
    constraint CUENTA_FINANCIERA_INSTITUCION_id_fk
        foreign key (institucion_id) references INSTITUCION_FINANCIERA (id)
);

create table TRANSFERENCIA_BANCARIA
(
    id                        bigint auto_increment
        primary key,
    cuenta_financiera_origen  bigint        null,
    cuenta_financiera_destino bigint        null,
    monto_transferido         double(12, 4) null,
    motivo                    longtext      null,
    constraint TRANSFERENCIA_BANCARIA_CUENTA_FINANCIERA_id_fk
        foreign key (cuenta_financiera_origen) references CUENTA_FINANCIERA (id),
    constraint TRANSFERENCIA_BANCARIA_CUENTA_FINANCIERA_id_fk_2
        foreign key (cuenta_financiera_destino) references CUENTA_FINANCIERA (id)
);

create table dummy
(
    texto varchar(255) null
);