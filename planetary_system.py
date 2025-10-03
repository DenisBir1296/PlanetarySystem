import numpy as np



# эйлера-крамера
'''
@jit(nopython=True)
def calc(n, position, velocity, mass, resistance, g, dt):
    for t in range(n):
        for i in range(len(mass)):
            a = g * mass
            b = np.power(np.power(position[0] - position[0][i], 2) + np.power(position[1] - position[1][i], 2), 3. / 2.)
            a[i], b[i] = 0., 1.
            a /= b
            velocity[0][i] += (np.sum((position[0] - position[0][i]) * a) - velocity[0][i] * resistance[i]) * dt
            velocity[1][i] += (np.sum((position[1] - position[1][i]) * a) - velocity[1][i] * resistance[i]) * dt

        position[0] += velocity[0] * dt
        position[1] += velocity[1] * dt
'''


class planetary_system:

    def __init__(self, dt, g):
        self.dt = dt
        self.g = g

        self.time = 0.
        # self.next_step = 20. * dt if next_step is None else next_step

        self.x_position = np.empty(0, dtype=np.float64)
        self.x_velocity = np.empty(0, dtype=np.float64)

        self.y_position = np.empty(0, dtype=np.float64)
        self.y_velocity = np.empty(0, dtype=np.float64)

        self.mass = np.empty(0, dtype=np.float64)
        self.resistance = np.empty(0, dtype=np.float64)

    def add(self, position, velocity, m, r=0.):
        self.x_position = np.append(self.x_position, position[0])
        self.y_position = np.append(self.y_position, position[1])

        self.x_velocity = np.append(self.x_velocity, velocity[0])
        self.y_velocity = np.append(self.y_velocity, velocity[1])

        self.mass = np.append(self.mass, m)
        self.resistance = np.append(self.resistance, r)

    def next(self, n=1):
        """
        time = self.next_step if time is None else time

        self.time += int((time) / self.dt) * self.dt

        calc(int(time / self.dt), [self.x_position, self.y_position], [self.x_velocity, self.y_velocity], self.mass,
             self.resistance, self.g, self.dt)"""
        for t in range(n):
            self.time += self.dt
            for i in range(len(self.mass)):
                a = self.g * self.mass
                b = pow(pow(self.x_position - self.x_position[i], 2) + pow(self.y_position - self.y_position[i], 2),
                        3. / 2.)
                a[i], b[i] = 0., 1.
                a /= b
                self.x_velocity[i] += sum((self.x_position - self.x_position[i]) * a) * self.dt
                self.y_velocity[i] += sum((self.y_position - self.y_position[i]) * a) * self.dt

            self.x_position += self.x_velocity * self.dt
            self.y_position += self.y_velocity * self.dt
            '''

    
    def animate(self, max_size=300, plot_size=None):
        if plot_size is None:
            plot_size = 1.2*max(abs(self.x_position + 1j*self.y_position))
        self.fig, self.ax = plt.subplots()
        sc_size = max_size*np.log(self.mass + 1.)/np.log(max(self.mass) + 1.)
        self.sc = self.ax.scatter(self.x_position, self.y_position, s=sc_size, c=np.linspace(1., 0., len(self.mass)))
        self.ax.set_xlim(-plot_size,plot_size)
        self.ax.set_ylim(-plot_size,plot_size)
        self.ax.set_aspect('equal')
        
        plt.grid(True)

        def anim(i):
            self.sc.set_offsets(np.stack([self.x_position, self.y_position]).T)
            self.next(0.2)
            return self.sc,

        self.ani = matplotlib.animation.FuncAnimation(self.fig, anim, frames=7, interval=20, blit=True) 
        return self.ani
    
    def show(self, max_size=300, plot_size=None):
        if plot_size is None:
            plot_size = 1.2*max(abs(self.x_position + 1j*self.y_position))
        sc_size = max_size*np.log(self.mass + 1.)/np.log(max(self.mass) + 1.)
        plt.scatter(self.x_position, self.y_position, s=sc_size, c=np.linspace(1., 0., len(self.mass)))
        plt.xlim(-plot_size,plot_size)
        plt.ylim(-plot_size,plot_size)
        plt.gca().set_aspect('equal')
        plt.grid(True)
        plt.show()'''

    def balancing_impulse(self):
        impulse = np.sum(self.x_velocity * self.mass)
        self.x_velocity -= impulse / np.sum(self.mass)

        impulse = np.sum(self.y_velocity * self.mass)
        self.y_velocity -= impulse / np.sum(self.mass)

    def balancing_mass(self):
        center_of_mass = self.get_center_of_mass()
        self.x_position -= center_of_mass[0]
        self.y_position -= center_of_mass[1]

    def get_center_of_mass(self):
        mass_sum = np.sum(self.mass)
        return np.sum(self.x_position * self.mass) / mass_sum, np.sum(self.y_position * self.mass) / mass_sum

    def count_of_planet(self):
        return len(self.mass)

    def get_planet(self, i):
        return (self.x_position[i], self.y_position[i]), (self.x_velocity[i], self.y_velocity[i]), self.mass[i]

    def __str__(self):
        return "".join([f'{n}.  m = {m}, pos = ({x}, {y}), vel = ({vx}, {vy})\n' for n, m, x, y, vx, vy in
                        zip(range(len(self.mass)), self.mass, self.x_position, self.y_position, self.x_velocity,
                            self.y_velocity)])


class planetary_system_arr(planetary_system):

    def __init__(self, pls, parameters, step=720000.):
        super().__init__(float(parameters['step']), float(parameters['g']))

        self.n = int(step / self.dt)
        if self.n == 0:
            self.n = 1

        for p in pls:
            self.add((float(p['x pos']), float(p['y pos'])),
                     (float(p['x vel']), float(p['y vel'])),
                     float(p['m']), float(p['res']))

        if parameters['bal mass']:
            self.balancing_mass()

        if parameters['bal impl']:
            self.balancing_impulse()

        self.count = int(float(parameters['time']) / self.dt) // self.n

    def calculate(self, func):

        result = {'pos': np.empty((2, self.count_of_planet(), self.count), dtype=float),
                  'vel': np.empty((2, self.count_of_planet(), self.count), dtype=float),
                  't': np.empty(self.count, dtype=float),
                  'm': self.mass,
                  'res': self.resistance,
                  'count': self.count}

        def save(k):
            result['pos'][0, :, k], result['pos'][1, :, k] = self.x_position, self.y_position
            result['vel'][0, :, k], result['vel'][1, :, k] = self.x_velocity, self.y_velocity
            result['t'][k] = self.time

        save(0)
        for j in range(1, self.count):
            if not func(j)[0]:
                result['count'] = j
                break
            self.next(self.n)
            save(j)
        return result
