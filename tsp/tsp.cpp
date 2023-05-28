#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <vector>
#include <cstring>
#include <stdio.h>
#include <ctime>

struct Point
{
public:
    int x;
    int y;

public:
    double distance_to(const Point &other)
    {
        return sqrt((other.x - x) * (other.x - x) + (other.y - y) * (other.y - y));
    }
};

class PointsCycle
{
private:
    int count;
    Point *points;
    std::vector<int> order;
    double cached_length;
    bool cached_length_valid;

public:
    PointsCycle(Point *points, int count)
    {
        this->count = count;
        this->points = points;

        // initialize with an "identity" ordering
        order.reserve(count);
        for (int i = 0; i < count; i++)
        {
            order.push_back(i);
        }

        cached_length_valid = false;
    }

    const std::vector<int> &getOrder() const
    {
        return order;
    }

    /// @brief Swaps two edges in the cycle, reversing the order of one
    /// part of the cycle to preserve continuity.
    /// @param a The index of the first point of the first edge to swap.
    /// @param c The index of the first point of the second edge to swap.
    void swap(int a, int c)
    {
        if (a < c)
        {
            std::reverse(order.begin() + a + 1, order.begin() + c + 1);
        }
        else
        {
            std::reverse(order.begin() + c + 1, order.begin() + a + 1);
        }

        cached_length_valid = false;
    }

    /// @brief Calculates the change in cycle length if a swap is
    /// performed.
    /// @param a The index of the first point of the first swapped edge.
    /// @param c The index of the first point of the second swapped edge.
    /// @return The change in the length of the cycle.
    double calculate_swap_length_change(int a, int c) const
    {
        int b = a < count - 1 ? a + 1 : 0;
        int d = c < count - 1 ? c + 1 : 0;

        // clang-format off
        return points[order[a]].distance_to(points[order[c]])
            + points[order[b]].distance_to(points[order[d]])
            - points[order[a]].distance_to(points[order[b]])
            - points[order[c]].distance_to(points[order[d]]);
        // clang-format on
    }

    /// @brief Calculates the length of the cycle.
    /// @return The length of the cycle.
    double calculate_length()
    {
        if (!cached_length_valid)
        {
            cached_length = 0;
            for (int i = 0; i < count - 1; i++)
            {
                cached_length += points[order[i]].distance_to(points[order[i + 1]]);
            }
            cached_length += points[order[count - 1]].distance_to(points[order[0]]);
            cached_length_valid = true;
        }

        return cached_length;
    }
};

__attribute__((constructor))
void constructor()
{
    srand(time(NULL));
}

extern "C" int *approximate_tsp(Point *points, size_t points_count, int temperature_iteration_count, int iteration_count)
{
    // begin with an unchanged order
    PointsCycle best_cycle(points, points_count);

    if (points_count < 4)
    {
        // only one possible cycle and cannot perform any swaps
        temperature_iteration_count = 0;
    }

    PointsCycle cycle(points, points_count);
    double start_temperature = cycle.calculate_length() * 100;
    double end_temperature = cycle.calculate_length() / points_count / 100;
    for (int temperature_iteration = 0; temperature_iteration < temperature_iteration_count; temperature_iteration++)
    {
        double temperature = start_temperature * pow(end_temperature / start_temperature, (double)temperature_iteration / (temperature_iteration_count - 1));
        for (int iteration = 0; iteration < iteration_count; iteration++)
        {
            // randomly pick existing edges (a, b) and (c, d),
            // where a, b, c, d are indices into the order array.
            // however, b and d do not need to be calculated here

            int a = rand() % points_count;

            int c;
            {
                int a_previous = a >= 1 ? a - 1 : points_count - 1;
                int a_next = a < points_count - 1 ? a + 1 : 0; // == b
                do
                {
                    c = rand() % points_count;
                } while (c == a_previous || c == a || c == a_next);
            }

            double length_change = cycle.calculate_swap_length_change(a, c);
            bool make_swap = length_change < 0;
            if (!make_swap)
            {
                // make swap with a certain probability, despite worsened length
                double r = (double)rand() / RAND_MAX;
                double probability = exp(-length_change / temperature);
                make_swap = r < probability;
            }

            if (make_swap)
            {
                cycle.swap(a, c);
            }

            if (cycle.calculate_length() < best_cycle.calculate_length())
            {
                best_cycle = cycle;
            }
        }
    }

    int *best_order = (int *)malloc(points_count * sizeof(int));
    for (int i = 0; i < points_count; i++)
    {
        best_order[i] = best_cycle.getOrder()[i];
    }
    return best_order;
}
