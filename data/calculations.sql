-- Número total de registros en el PMH 2S/2018
select
    count(id)
from
    seguridad.pmh_dn
where
    anno = 2018 and
    semestre = 2;
-- Card(sample) = 583409

-- Partículas
-- DA|DE|DE LA|DE LAS|DE LOS|DEL|DI|DL|DO|DOS|EL|EP|I|LA|LAS|LOS|LE|SAN|VAN

-- Número de registros con nombre no compuesto
select
    count(id)
from
    seguridad.pmh_dn
where
    regexp_like(nomb, '^[A-ZÑÁÉÍÓÚÄËÏÖÜÂÊÎÔÛ]+$') and
    anno = 2018 and
    semestre = 2;
-- Card(simple first_name) = 379510
-- P(first_name -> last_name_1) = 379510 / 583409 = 0.650504192
-- Card(composed first_name) = 583409 - 379510 = 203899

-- Registros con nombre compuesto que contienen partículas
select
    count(id)
from
    seguridad.pmh_dn
where
    regexp_like(nomb, '.* (DE|DEL|LOS|LAS|LA|DO|DU|Y) .*') and
    anno = 2018 and
    semestre = 2;
-- Card(composed first_name with particles) = 5979
-- Card(composed first_name without particles) = 203899 - 5979 = 197920
-- P(first_name -> first_name) = 197920 / 583409 = 0.339247423

-- Nombre con partículas compuestas
select
    count(id)
from
    seguridad.pmh_dn
where
    regexp_like(nomb, '.* (DE|DEL|LO|LOS|LAS|LA|DO|DU|Y) .*') and
    (nomb like '% DE LOS %' or nomb like '% DE LAS %' or nomb like '% DE LA %') and
    anno = 2018 and
    semestre = 2;
-- Card(composed first_name with composed particles) = 961
-- Card(composed first_name with single particle) = 5979 - 961 = 5018
-- P(first_name -> particle) = 5979 / 583409 = 0.010248385
-- P(particle -> first_name) = 5018 / 583409 = 0.00860117
-- P(particle -> particle) = 961 / 583409 = 0.001647215

-- Número de registros con partícula en apellido1
select
    count(id)
from
    seguridad.pmh_dn
where
    part1 is not null and
    anno = 2018 and
    semestre = 2;

-- Número de registros con primer apellido no compuesto y apellido2 no es nulo
select
    count(id)
from
    seguridad.pmh_dn
where
    regexp_like(ape1, '^[A-ZÑÁÉÍÓÚÄËÏÖÜÂÊÎÔÛ]+$') and
    ape2 is not null and
    part1 is null and
    anno = 2018 and
    semestre = 2;
-- Card(simple last_name_1 and last_name_2 not null) = 540529
-- P(last_name_1 -> last_name_2) = 540529 / 583409 = 0.926500962

-- Número de registros con primer apellido no compuesto y apellido2 es nulo
select
    count(id)
from
    seguridad.pmh_dn
where
    regexp_like(ape1, '^[A-ZÑÁÉÍÓÚÄËÏÖÜÂÊÎÔÛ]+$') and
    ape2 is null and
    anno = 2018 and
    semestre = 2;
-- Card(simple last_name_1 and last_name_2 is null) = 19692
-- P(last_name_1 -> END) = 19692 / 583409 = 0.033753336

-- Card(composed last_name_1) = 583409 - 549704 - 19692 = 14013

-- P(last_name_1 -> last_name_1) = 14013 / 583409 = 0.02401917

-- Número de registros con segundo apellido no compuesto
select
    count(id)
from
    seguridad.pmh_dn
where
    regexp_like(ape2, '^[A-ZÑÁÉÍÓÚÄËÏÖÜÂÊÎÔÛ]+$') and
    anno = 2018 and
    semestre = 2;
-- Card(simple last_name_2) = 550785
-- P(last_name_2 -> END) = 550785 / 583409 = 0.944080396
-- Card(composed last_name_2) = 583409 - 550785 = 32624
-- P(last_name_2 -> last_name_2) = 32624 / 583409 = 0.055919604

-- Obtención de listados de nombres y apellidos
select
    nomb
from
    seguridad.pmh_dn
where
    nomb is not null and
    anno = 2018 and
    semestre = 2;

select
    part1, ape1
from
    seguridad.pmh_dn
where
    ape1 is not null and
    anno = 2018 and
    semestre = 2;

select
    part2, ape2
from
    seguridad.pmh_dn
where
    ape2 is not null and
    anno = 2018 and
    semestre = 2;