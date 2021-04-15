import concurrent.futures

import multiprocessing as mp

import time



def mano_sum(inf, sup):

    return sum(range(inf, sup))



def par_sum(inf, sup, pool=None):

    if not pool:

        with concurrent.futures.ProcessPoolExecutor() as capataz:

            trabajo_a_realizar = par_sum(inf, sup, pool=capataz)

            return sum(trabajo_completado.result() for trabajo_completado in concurrent.futures.as_completed(trabajo_a_realizar))

    else:

        if sup - inf <= 3_000_000:  # caso base

            return [pool.submit(sum, range(inf, sup))]

        else:

            mitad = (sup + inf) // 2

            parte_izq = par_sum(inf, mitad, pool=pool)

            parte_der = par_sum(mitad, sup, pool=pool)

            return parte_izq + parte_der





if __name__ == '__main__':

    NUM_EVAL_RUNS = 1

    SUM_VALUE = 3_000_000_000



    print('Calculando el resultado sin usar todos los cores...')

    resultado_a_mano = mano_sum(1, SUM_VALUE)

    tiempo_a_mano = 0

    for i in range(NUM_EVAL_RUNS):

        inicio = time.perf_counter()

        mano_sum(1, SUM_VALUE)

        tiempo_a_mano += time.perf_counter() - inicio

    tiempo_a_mano /= NUM_EVAL_RUNS



    print('Calculando el resultado usando todos los cores......')

    resultado_a_toda_maquina = par_sum(1, SUM_VALUE)

    tiempo_a_toda_maquina = 0

    for i in range(NUM_EVAL_RUNS):

        inicio = time.perf_counter()

        par_sum(1, SUM_VALUE)

        tiempo_a_toda_maquina += time.perf_counter() - inicio

    tiempo_a_toda_maquina /= NUM_EVAL_RUNS



    print('\nTiempo_a_MANO: {:.2f} ms'.format(tiempo_a_mano * 1000))

    print('\nTiempo_a_toda_MAQUINA: {:.2f} ms'.format(tiempo_a_toda_maquina * 1000))

    print('\n\nRelación entre tiempo a MANO y tiempo a toda MAQUINA: {:.2f}'.format(tiempo_a_mano / tiempo_a_toda_maquina))

    print('\nRelación entre la computación usando a mano VS a toda máquina: {:.2f}%'.format(100 * (tiempo_a_mano / tiempo_a_toda_maquina) / mp.cpu_count()))