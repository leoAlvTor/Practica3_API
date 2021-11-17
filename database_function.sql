create or replace
    definer = monty@`%` function realizar_transferencia(cedula varchar(255), institucion_destino varchar(255),
                                                        origen varchar(255), destino varchar(255), monto double(12, 4),
                                                        motivo_transferencia longtext) returns int
BEGIN

    declare saldo_actual double(12, 4);
    declare institucion_origen int(10);
    declare institucion_destino int(10);

    declare count_institucion_financiera int;
    declare count_cuenta_financiera int;

    select saldo_actual
    into saldo_actual
    from CUENTA_FINANCIERA
    where CUENTA_FINANCIERA.cliente_cedula = cedula
      and CUENTA_FINANCIERA.numero_cuenta = origen;

    if saldo_actual < monto then
        return -1; -- Saldo insuficiente
    end if;

    select count(*) into count_institucion_financiera from INSTITUCION_FINANCIERA where nombre = institucion_destino;
    insert into dummy values (count_institucion_financiera);
    If count_institucion_financiera = 0 then
        return -2; -- La institucion destino no existe
    end if;

    select institucion_id
    into institucion_origen
    from CUENTA_FINANCIERA
    where cliente_cedula = cedula
      and CUENTA_FINANCIERA.numero_cuenta = origen;
    select id into institucion_destino from INSTITUCION_FINANCIERA where nombre = institucion_destino;

    select count(*)
    into count_cuenta_financiera
    from CUENTA_FINANCIERA
    where numero_cuenta = destino
      and institucion_id = institucion_destino;
    if count_cuenta_financiera = 0 then
        return -3; -- La cuenta financiera no existe en base al numero de cuenta y a la institucion.
    end if;

    update CUENTA_FINANCIERA
    set saldo_actual = saldo_actual - monto
    where cliente_cedula = cedula
      and numero_cuenta = origen;
    update CUENTA_FINANCIERA
    set saldo_actual = saldo_actual + monto
    where numero_cuenta = destino
      and institucion_id = institucion_destino;

    insert into TRANSFERENCIA_BANCARIA(cuenta_financiera_origen, cuenta_financiera_destino, monto_transferido, motivo)
    values (institucion_origen, institucion_destino, monto, motivo_transferencia);

    return 0;

end;